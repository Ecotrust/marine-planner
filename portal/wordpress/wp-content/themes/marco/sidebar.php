				<div id="sidebar1" class="fluid-sidebar sidebar span4" role="complementary">
					<h3><a href="<?php echo get_bloginfo('wpurl'); ?>/learn">Learn</a></h3>
					<ul class="unstyled">
						 <?php
						// Set up the objects needed
						//$my_wp_query = new WP_Query();
						//$all_wp_pages = $my_wp_query->query(array('post_type' => 'page'));

						// Get the page as an Object
						$learn =  get_page_by_title('Learn');

						// Filter through all pages and find Learn's children
						$learn_children = get_pages( array( 'child_of' => $learn->ID) );

						echo "<ul class='styled'>";
						foreach ($learn_children as $child) {
							printf("<li><a href='%s/learn/%s'>%s</a></li>", get_bloginfo('wpurl'), $child->post_name, $child->post_title);

	    				}
	    				echo "</ul>";
						// echo what we get back from WP to the browser
						//echo '<pre>'.print_r($learn_children,true).'</pre>';
						?>
					</ul>
					<h3><a href="<?php echo get_bloginfo('wpurl'); ?>/explore">Explore</a></h3>
					<ul class="unstyled">
						<li><a href="<?php echo get_bloginfo('wpurl'); ?>">Data Catalog</a></li>
						<li><a href="<?php echo get_bloginfo('wpurl'); ?>">Data Priorities</a></li>
					</ul>
					<h3><a href="<?php echo get_bloginfo('wpurl'); ?>/visualize">Visualize</a></h3>
					<ul class="unstyled">
						<li><a href="http://dev.marco.marineplanning.org">Planning Tool</a></li>
						<li><a href="<?php echo get_bloginfo('wpurl'); ?>">Feature</a></li>
						<li><a href="<?php echo get_bloginfo('wpurl'); ?>">Feature</a></li>
						<li><a href="<?php echo get_bloginfo('wpurl'); ?>">Feature</a></li>
						<li><a href="<?php echo get_bloginfo('wpurl'); ?>">Feature</a></li>
					</ul>
		
				</div>