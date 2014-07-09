# example recipe
# ============



execute "clean it" do
    command "apt-get clean -y"
end

execute "update package index" do
    command "apt-get update"
end

group "deploy" do
    gid 123
end

if node[:user] == "vagrant"

    user "vagrant" do
        group "deploy"
    end

    template "/home/vagrant/.bashrc" do
        source "bashrc.erb"
        owner "vagrant"
    end
else
    node[:users].each do |u|
        user u[:name] do
            username u[:name]
            shell "/bin/bash"
            home "/home/#{u[:name]}"
            group "deploy"
        end

        directory "/home/#{u[:name]}" do
            owner u[:name]
            group "deploy"
            mode 0700
        end

        directory "/home/#{u[:name]}/.ssh" do
            owner u[:name]
            group "deploy"
            mode 0700
        end

        template "/home/#{u[:name]}/.bashrc" do
            source "bashrc.erb"
            owner u[:name]
            mode 0700
        end

        # cookbook_file "/home/#{u[:name]}/.profile" do
            # source "profile"
            # owner u[:name]
            # mode 0700
        # end

        execute "authorized keys" do
            command "echo #{u[:key]} > /home/#{u[:name]}/.ssh/authorized_keys"
        end
    end

    cookbook_file "/etc/sudoers" do
        source "sudoers"
        mode 0440
    end
    
    package "dos2unix"
    execute "authorized keys" do
        command "dos2unix /etc/sudoers"
    end
end

directory "/usr/local/apps" do
    owner "www-data"
    group "deploy"
    mode 0770
end

directory "/usr/local/apps/marine-planner" do
    owner "www-data"
    group "deploy"
    mode 0770
end


directory "/usr/local/apps/marine-planner/mp" do
    owner "www-data"
    group "deploy"
    mode 0770
end


directory "/usr/local/venv" do
    owner "www-data"
    group "deploy"
    mode 0770
end

# ssh  ------------------------------------------------------------------------

cookbook_file "/etc/ssh/sshd_config" do
    source "sshd_config"
end

execute "restart ssh" do
    command "service ssh restart"
end

package "vim"
package "python-software-properties"
package "ntp"
package "curl"
package "htop"
package "mosh"
package "mercurial"
package "subversion"
package "csstidy"
package "unzip"
package "python-pip"
package "python-dev"

include_recipe "openssl"
include_recipe "build-essential"
include_recipe "git"
include_recipe "python"
include_recipe "apt"
include_recipe "nginx"
include_recipe "postgresql::server"
#include_recipe "supervisor"

# package "supervisor"

# marine planner specific
package "postgresql-#{node[:postgresql][:version]}-postgis"

execute "add mapnik ppa" do
    command "/usr/bin/add-apt-repository -y ppa:mapnik/nightly-2.0 && /usr/bin/apt-get update"
    not_if "test -x /etc/apt/sources.list.d/mapnik-nightly-2_0-*.list"
end

package "libmapnik"
package "mapnik-utils"
package "python-mapnik"
package "python-kombu"
package "python-gdal"
package "python-imaging"
package "python-numpy"
package "python-psycopg2"
package "redis-server"

cookbook_file "/usr/share/proj/epsg" do
    source "epsg"
    mode 0755
end

if node[:user] == "vagrant"
    template "/vagrant/mp/settings_local.py" do
        source "settings_local.erb"
        owner "vagrant"
        mode 0760
    end
else
    template "/usr/local/apps/marine-planner/mp/settings_local.py" do
        source "settings_deploy.erb"
         mode 0760
        owner "www-data"
    end
end


template "/etc/init/app.conf" do
    source "app.conf.erb"
end

execute "restart app" do
    command "sudo service app restart"
end


cookbook_file "/etc/postgresql/#{node[:postgresql][:version]}/main/pg_hba.conf" do
    source "pg_hba.conf"
    owner "postgres"
end

execute "restart postgres" do
    command "sudo /etc/init.d/postgresql restart"
end
execute "restart nginx" do
    command "sudo /etc/init.d/nginx restart"
end

# psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
# psql -d template_postgis -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql

execute "create database" do
    command "createdb -U postgres -T template0 -O postgres #{node[:dbname]} -E UTF8 --locale=en_US.UTF-8"
    not_if "psql -U postgres --list | grep #{node[:dbname]}"
end

execute "load postgis" do
    command "psql  -U postgres -d #{node[:dbname]} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql"
    not_if "psql -U postgres #{node[:dbname]} -P pager -t --command='SELECT tablename FROM pg_catalog.pg_tables'|grep spatial_ref_sys"
end
execute "load spatial references" do
    command "psql -U postgres  -d #{node[:dbname]} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql"
    not_if "psql -U postgres #{node[:dbname]} -P pager -t --command='SELECT srid FROM  spatial_ref_sys' |grep 900913"
end

python_virtualenv "/usr/local/venv/marine-planner" do
    action :create
    group "deploy"
    options "--system-site-packages"
    if node[:user] == "vagrant"
        owner "vagrant"
    else
        owner "www-data"
    end
end
link "/usr/venv" do
  to "/usr/local/venv"
end


# map proxy stuff
template "/etc/init/mapproxy.conf" do
    source "mapproxy.conf.erb"
end

if node[:user] == "vagrant"
    template "/vagrant/proxy/mapproxy.yaml" do
        source "mapproxy.yaml.erb"
        owner node[:user]
        group "deploy"
        mode 0700
    end
else
    template "/usr/local/apps/marine-planner/proxy/mapproxy.yaml" do
        source "mapproxy.yaml.erb"
        owner node[:user]
        group "deploy"
        mode 0700
    end
end

directory "/var/log/mapproxy" do
    owner node[:user]
    group "deploy"
    mode 0700
end