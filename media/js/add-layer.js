(function() {


	function newLayerModel() {
		var self = this;
		self.name = ko.observable();
		self.url = ko.observable();
		self.layer_type = ko.observable();
		self.theme = ko.observable();
		self.arcgis_layers = ko.observable();
		self.wms_slug = ko.observable();
		return this;
	}
	app.viewModel.newLayer = ko.observable();

	app.viewModel.showAddLayerModal = function() {
		app.viewModel.newLayer(new newLayerModel());
		$('#add-layer-modal').modal('show');
	};

	app.viewModel.createLayer = function() {
		var data, theme_uri, theme = app.viewModel.newLayer().theme();

		data = {
			name: app.viewModel.newLayer().name(),
			url: app.viewModel.newLayer().url(),
			layer_type: app.viewModel.newLayer().layer_type(),
			arcgis_layers: app.viewModel.newLayer().arcgis_layers(),
			wms_slug: app.viewModel.newLayer().wms_slug()
		};
		if (theme.is_toc_theme) {
			theme_uri = "/api/v1/toctheme/" + theme.id + '/';
			data.toc_themes = [theme_uri];
		} else {
			theme_uri = "/api/v1/theme/" + theme.id + '/';
			data.themes = [theme_uri];
		}
		if (data.layer_type === 'ArcRest') {
			data.url = data.url + '/export';
			if (! data.arcgis_layer) {
				data.arcgis_layer = 0;
			}
		}
		$.ajax({
			beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", app.csrftoken);
            },
			type: "POST",
			url: "/api/v1/layer/",
			contentType: "application/json; charset=utf-8",
			dataType: 'json',
			processData: false,
			data: JSON.stringify(data)
		})
			.success(function(data) {
				var layer = new layerModel(data);
				$.each(app.viewModel.themes(), function (i, theme) {
					var data_theme = theme.is_toc_theme ? data.toc_themes[0]: data.themes[0];
					if (theme.name === data_theme.display_name) {
						theme.layers.push(layer);
						if (! theme.isOpenTheme()) {
							theme.setOpenTheme();
						}
						layer.activateLayer();
					}
				});
			});
	};

})();