
var madrona = { 
    onShow: function(callback) { callback(); },
    setupForm: function($form) {
        //var submitted = false;
    
        $form.find('.btn-submit').hide();

        $form.find('label').each(function (i, label) {
            if ($(label).find('input[type="checkbox"]').length) {
                $(label).addClass('checkbox');
            }
        });
        
        $form.closest('.panel').on('click', '.cancel_button', function(e) {
            app.viewModel.scenarios.reset({cancel: true});
        });

        $form.closest('.panel').on('click', '.submit_button', function(e) {
            e.preventDefault();
            var name = $('#id_name').val();
            if ($.trim(name) === "") {  
                $('#invalid-name-message').show();
                return false;
            } 
            //submitted = true;
            submitForm($form);
        }); 
        
        //no longer needed...? (if it was going here it meant there was a problem)
        /*
        $form.submit( function() {
            var name = $('#id_name').val();
            if ($.trim(name) === "") {  
                $('#invalid-name-message').show();
                return false;
            } 
            if (!submitted) {
                submitForm($form);
            }
        });
        */
        submitForm = function($form) {
            //var $form = $(this).closest('.panel').find('form'),
            var url = $form.attr('action'),
                $bar = $form.closest('.tab-pane').find('.bar'),
                data = {},
                barTimer;
                
            //progress bar
            barTimer = setInterval(function () {
                var width = parseInt($bar.css('width').replace('px', ''), 10) + 5,
                    barWidth = parseInt($bar.parent().css('width').replace('px',''), 10);
                
                if (width < barWidth) {
                    $bar.css('width', width + "px");    
                } else {
                    clearInterval(barTimer);
                }
            }, 500);
            
            
            $form.find('input,select,textarea').each( function(index, input) {
                var $input = $(input);
                if ($input.attr('type') === 'checkbox') {
                    if ($input.attr('checked')) {
                        data[$input.attr('name')] = 'True';
                    } else {
                        data[$input.attr('name')] = 'False';
                    }
                } else {
                    data[$input.attr('name')] = $input.val();
                }
            });



            app.viewModel.scenarios.scenarioForm(false);
            app.viewModel.scenarios.loadingMessage("Creating Design");
            
            $.ajax( {
                url: url,
                data: data,
                type: 'POST',
                dataType: 'json',
                success: function(result) {
                    app.viewModel.scenarios.addScenarioToMap(null, {uid: result['X-Madrona-Show']});                    
                    app.viewModel.scenarios.loadingMessage(false);
                    clearInterval(barTimer);
                },
                error: function(result) {
                    app.viewModel.scenarios.loadingMessage(null);
                    clearInterval(barTimer);
                    if (result.status === 400) {
                        $('#scenario-form').append(result.responseText);
                        app.viewModel.scenarios.scenarioForm(true);
                    } else {
                        app.viewModel.scenarios.errorMessage(result.responseText.split('\n\n')[0]);
                    }
                }
            });
        };
        
    }
}; // end madrona init


function scenarioFormModel(options) {
    var self = this;
    
    //Parameters    
    self.fish_abundance = ko.observable(false);
    self.fish_abundance_min = ko.observable(0);
    self.fish_abundance_max = ko.observable(0);
    
    self.fish_richness = ko.observable(false);
    self.fish_richness_min = ko.observable(0);
    self.fish_richness_max = ko.observable(0);
    
    self.coral_richness = ko.observable(false);
    self.coral_richness_min = ko.observable(0);
    self.coral_richness_max = ko.observable(0);

    self.coral_density = ko.observable(false);
    self.coral_density_min = ko.observable(0);
    self.coral_density_max = ko.observable(0);

    self.coral_size = ko.observable(false);
    self.coral_size_min = ko.observable(0);
    self.coral_size_max = ko.observable(0);

    self.inlet_distance = ko.observable(false);
    self.inlet_distance_min = ko.observable(0);
    self.inlet_distance_max = ko.observable(0);

    self.shore_distance = ko.observable(false);
    self.shore_distance_min = ko.observable(0);
    self.shore_distance_max = ko.observable(0);

    var initial_leaseblocks_left = app.viewModel.scenarios.leaseblockList.length || 3426;
    self.leaseblocksLeft = ko.observable(initial_leaseblocks_left);
    self.showLeaseblockSpinner = ko.observable(false);
    
    self.isLeaseblockLayerVisible = ko.observable(false);
    self.isLeaseblockLayerVisible.subscribe( function() {
        if ( self.isLeaseblockLayerVisible() ) {
            self.showRemainingBlocks();
        } else {
            self.hideLeaseblockLayer();
        }
    });
        
    self.activateLeaseblockLayer = function() {
        self.isLeaseblockLayerVisible(true);
        //self.showRemainingBlocks();
    };
    
    self.deactivateLeaseblockLayer = function() {
        self.isLeaseblockLayerVisible(false);
        //remove from attribute list (if it's there)
        app.viewModel.removeFromAggregatedAttributes(app.viewModel.scenarios.scenarioLeaseBlocksLayerName);
        app.viewModel.updateAggregatedAttributesOverlayWidthAndScrollbar();
        //self.hideLeaseblockLayer();
    };
    
    self.lastChange = (new Date()).getTime();
    
    /** Toggle an input div. */
    self.toggleParameter = function(param) {
        var param_bool = self[param];
        var param_element = $('#id_' + param);
        var param_widget = $('#' + param + '_widget');
        
        if (param_bool()) {
            param_bool(false);
            param_element.removeAttr('checked');
            param_widget.css('display', 'none');
            self.removeFilter(param);
        }
        else {
            var min;
            var max;
            var param_element_min = $('#id_' + param + '_min')[0];
            if (param_element_min) {
                min = param_element_min.value;
            }
            var param_element_max = $('#id_' + param + '_max')[0];
            if (param_element_max) {
                max = param_element_max.value;
            }
            
            param_bool(true);
            param_element.attr('checked', 'checked');
            param_widget.css('display', 'block');
            
            self.updateFilters(param, min, max);
        }
        
        self.updateDesignScrollBar();
        self.updateFiltersAndLeaseBlocks();
        self.updateRemainingBlocks();
    };
    
    /** Returns a partial function which calls toggleParameter.
        var fn = parameterToggler('wind');
        fn();
     */
    self.parameterToggler = function(param) {
        return function() {
            self.toggleParameter(param);
        }
    }
    
    self.filters = {};
    self.masterFilter = new OpenLayers.Filter.Logical({
        type: OpenLayers.Filter.Logical.AND,
        filters: []
    });
    
    /** Add a filter. 
    Filters are value name (e.g., bathy_avg), the min value (e.g., 30), and 
    the max value (e.g., 130). 
    If you want a one-sided relation of value greater than min (param > min), 
    then pass null for max 
    If you want a one-sided relation of value less than max (param < max), 
    then pass null for min 
    */
    self.updateFilters = function(param_name, min, max) {
        var filter; 
        
        if (Number(min) != min) {
            min = null; 
        }
        else {
            min = Number(min);
        }
        if (Number(max) != max) {
            max = null;
        }
        else {
            max = Number(max);
        }

        // exclude checkbox, == 0
        if (min == null && max == null) {
            filter = new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.EQUAL_TO,
                property: param_name,
                value: 0
            });
        }
        // less than filter
        else if (min == null) {
            filter = new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.LESS_THAN,
                property: param_name,
                value: max
            });
        }
        // greater than filter
        else if (max == null) {
            filter = new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.GREATER_THAN,
                property: param_name,
                value: min
            });
        }
        // between filter
        else {
            filter = new OpenLayers.Filter.Comparison({
                type: OpenLayers.Filter.Comparison.BETWEEN,
                property: param_name,
                lowerBoundary: min,
                upperBoundary: max,
            });
        }

        self.filters[param_name] = filter;
    }

    self.removeFilter = function(key) {
        delete self.filters[key];
    };
    
    self.updateFiltersAndLeaseBlocks = function() {
        return;
        self.updateLeaseblocksLeft();
    
    };
    
    self.updateLeaseblocksLeft = function() {
        return;
        var list = app.viewModel.scenarios.leaseblockList;
        var count = 0;
        
        self.masterFilter.filters = [];
        for (var f in self.filters) {
            self.masterFilter.filters.push(self.filters[f].clone());
        }
        
        for (var i = 0; i < list.length; i++) {
            if (self.masterFilter.evaluate(list[i])) {
                count++;
            }
        }

        self.leaseblocksLeft(count);
    };
    
    self.updateRemainingBlocks = function() {
        return;
        self.lastChange = (new Date()).getTime(); 
        setTimeout(function() {
            var newTime = (new Date()).getTime();
            if ( newTime - self.lastChange > 100 ) {
                self.showRemainingBlocks();
            }
        }, 200);
    };
    
    self.showRemainingBlocks = function() {
        return;
        if ( self.isLeaseblockLayerVisible() ) {
            self.showLeaseblockSpinner(true);
            if ( ! app.viewModel.scenarios.leaseblockLayer()) {
                app.viewModel.scenarios.loadLeaseblockLayer();
            } 
            var blockLayer = app.viewModel.scenarios.leaseblockLayer();
            
            blockLayer.styleMap.styles['default'].rules[0] = new OpenLayers.Rule({
                filter: self.masterFilter, 
                symbolizer: { strokeColor: '#fff' } 
            });
            
            self.showLeaseblockLayer(blockLayer);
        }
    };
    
    self.showLeaseblockLayer = function(layer) {
        return;
        if ( ! app.map.getLayersByName(app.viewModel.scenarios.leaseblockLayer().name).length ) {
            app.map.addLayer(app.viewModel.scenarios.leaseblockLayer());
        }
        //layer.layerModel.setVisible();
        layer.setVisibility(true);
        app.viewModel.updateAttributeLayers();
        //layer.refresh();
        layer.redraw();
    }
    
    self.hideLeaseblockLayer = function() {
        return;
        app.viewModel.scenarios.leaseblockLayer().setVisibility(false);
        //if ( app.map.getLayersByName(app.viewModel.scenarios.leaseblockLayer().name).length ) {
        //    app.map.removeLayer(app.viewModel.scenarios.leaseblockLayer());
        //}
        //remove the key/value pair from aggregatedAttributes
        app.viewModel.removeFromAggregatedAttributes(app.viewModel.scenarios.leaseblockLayer().name);
        app.viewModel.updateAttributeLayers();
    }
    
    self.updateDesignScrollBar = function() {
        var designsWizardScrollpane = $('#wind-design-form').data('jsp');
        if (designsWizardScrollpane === undefined) {
            $('#wind-design-form').jScrollPane();
        } else {
            setTimeout(function() {designsWizardScrollpane.reinitialise();},100);
        }
    };
    
    return self;
} // end scenarioFormModel


function scenarioModel(options) {
    var self = this;

    self.id = options.uid || null;
    self.uid = options.uid || null;
    self.name = options.name;
    self.featureAttributionName = self.name;
    self.description = options.description;
    self.shared = ko.observable();
    self.sharedByName = options.sharedByName || null;
    self.sharedByUsername = options.sharedByUsername;
    if (self.sharedByName && $.trim(self.sharedByName) !== '') {
        self.sharedByWho = self.sharedByName + ' (' + self.sharedByUsername + ')';
    } else {
        self.sharedByWho = self.sharedByUsername;
    }
    self.sharedBy = ko.observable();
    if (options.shared) {
        self.shared(true);
        self.sharedBy('Shared by ' + self.sharedByWho);
    } else {
        self.shared(false);
        self.sharedBy(false);
    }
    self.selectedGroups = ko.observableArray();
    self.sharedGroupsList = [];
    if (options.sharingGroups && options.sharingGroups.length) {
        self.selectedGroups(options.sharingGroups);
    } 
    self.sharedWith = ko.observable();
    self.updateSharedWith = function() {
        if (self.selectedGroups().length) {
            var groupNames = "Shared with " + self.selectedGroups()[0];
            for(var i=1; i<self.selectedGroups().length; i+=1) {
                groupNames += ", " + self.selectedGroups()[i];
            }
            self.sharedWith(groupNames);
        }
    };
    self.updateSharedWith();
    self.selectedGroups.subscribe( function() {
        self.updateSharedWith();
    });
    self.temporarilySelectedGroups = ko.observableArray();
    
    self.attributes = [];
    self.scenarioAttributes = options.attributes ? options.attributes.attributes : [];
    
    self.showingLayerAttribution = ko.observable(true);
    self.toggleLayerAttribution = function() {
        var layerID = '#' + app.viewModel.convertToSlug(self.name);
        if ( self.showingLayerAttribution() ) {
            self.showingLayerAttribution(false);
            $(layerID).css('display', 'none');
        } else {
            self.showingLayerAttribution(true);
            $(layerID).css('display', 'block');
        }
        //update scrollbar
        app.viewModel.updateAggregatedAttributesOverlayScrollbar();
    };
    
    //self.overview = self.description || 'no description was provided';
    self.constructInfoText = function() {
        var attrs = self.scenarioAttributes,
            output = '';

        for (var i=0; i< attrs.length; i++) {
            // if (attrs[i].title === 'Description') {
            //     output += attrs[i].data + '\n';
            // } else {
                output += attrs[i].title + ': ' + attrs[i].data + '\n';
            // }
        }  
        return output;
    };
    self.overview = self.constructInfoText();
        
    self.scenarioReportValues = options.attributes ? options.attributes.report_values : [];

    self.features = options.features;
    
    self.active = ko.observable(false);
    self.visible = ko.observable(false);
    self.defaultOpacity = options.opacity || 0.8;
    self.opacity = ko.observable(self.defaultOpacity);
    self.type = 'Vector';
    
    self.opacity.subscribe( function(newOpacity) {
        if ( self.layer ) {
            self.layer.styleMap.styles['default'].defaultStyle.strokeOpacity = newOpacity;
            self.layer.styleMap.styles['default'].defaultStyle.fillOpacity = newOpacity;
            self.layer.redraw();
        } else {
            //debugger;
        }
    });
    
    self.toggleActive = function(self, event) {
        var scenario = this;
        
        // start saving restore state again and remove restore state message from map view
        app.saveStateMode = true;
        app.viewModel.error(null);
        //app.viewModel.unloadedDesigns = [];
        
        //app.viewModel.activeLayer(layer);
        if (scenario.active()) { // if layer is active, then deactivate
            scenario.deactivateLayer();
        } else { // otherwise layer is not currently active, so activate
            scenario.activateLayer();
            //app.viewModel.scenarios.addScenarioToMap(scenario);
        }
    };
    
    self.activateLayer = function() {
        var scenario = this;
        app.viewModel.scenarios.addScenarioToMap(scenario);
        if (scenario.isDrawingModel ) {
            
        } else if ( scenario.isSelectionModel ) {
            for (var i=0; i < app.viewModel.scenarios.activeSelections().length; i=i+1) {
                if(app.viewModel.scenarios.activeSelections()[i].id === scenario.id) { 
                    app.viewModel.scenarios.activeSelections().splice(i,1);
                    i = i-1;
                }
            }
            app.viewModel.scenarios.activeSelections().push(scenario);
        }
    };
    
    self.deactivateLayer = function() {
        var scenario = this;
        
        scenario.active(false);
        scenario.visible(false);
        
        if ( scenario.isSelectionModel ) {
            var index = app.viewModel.scenarios.activeSelections().indexOf(scenario);
            app.viewModel.scenarios.activeSelections().splice(index, 1);
            app.viewModel.scenarios.reports.updateChart();
        }
        
        scenario.opacity(scenario.defaultOpacity);
        app.setLayerVisibility(scenario, false);
        app.viewModel.activeLayers.remove(scenario);
        
        app.viewModel.removeFromAggregatedAttributes(scenario.name);
            
        // //remove the key/value pair from aggregatedAttributes
        // delete app.viewModel.aggregatedAttributes()[scenario.name];
        // //if there are no more attributes left to display, then remove the overlay altogether
        // if ($.isEmptyObject(app.viewModel.aggregatedAttributes())) {
        //     app.viewModel.aggregatedAttributes(false);
        // }
        
    };
    
    self.editScenario = function() {
        var scenario = this;
        return $.ajax({
            url: '/features/scenario/' + scenario.uid + '/form/',
            success: function(data) {
                //$('#scenario-form').append(data);
                app.viewModel.scenarios.scenarioForm(true);
                $('#scenario-form').html(data);
                app.viewModel.scenarios.scenarioFormModel = new scenarioFormModel();
                var model = app.viewModel.scenarios.scenarioFormModel;
                
                ko.applyBindings(model, document.getElementById('scenario-form'));

                var parameters = [
                    'fish_abundance', 'fish_richness', 'coral_richness', 'coral_density', 
                    'coral_size', 'inlet_distance', 'shore_distance'
                ];

                for (var i = 0; i < parameters.length; i++) {
                    var id = '#id_' + parameters[i];
                    
                    if ($(id).is(':checked')) {
                        model.toggleParameter(parameters[i]);
                    }
                }

                model.updateFiltersAndLeaseBlocks();
            },
            error: function (result) {
                //debugger;
            }
        });
    };

    self.createCopyScenario = function() {
        var scenario = this;
    
        //create a copy of this shape to be owned by the user
        $.ajax({
            url: '/scenario/copy_design/' + scenario.uid + '/',
            type: 'POST',
            dataType: 'json',
            success: function(data) {
                //app.viewModel.scenarios.loadSelectionsFromServer();
                app.viewModel.scenarios.addScenarioToMap(null, {uid: data[0].uid});
            },
            error: function (result) {
                //debugger;
            }
        });
    };
        
    self.deleteScenario = function() {
        var scenario = this;
        
        //first deactivate the layer 
        scenario.deactivateLayer();
        
        //remove from activeLayers
        app.viewModel.activeLayers.remove(scenario);
        //remove from app.map
        if (scenario.layer) {
            app.map.removeLayer(scenario.layer);
        }
        //remove from scenarioList
        app.viewModel.scenarios.scenarioList.remove(scenario);
        //update scrollbar
        app.viewModel.scenarios.updateDesignsScrollBar();
        
        //remove from server-side db (this should provide error message to the user on fail)
        $.ajax({
            url: '/scenario/delete_design/' + scenario.uid + '/',
            type: 'POST',
            error: function (result) {
                //debugger;
            }
        });
    };
    
    self.visible = ko.observable(false);  
    
    // bound to click handler for layer visibility switching in Active panel
    self.toggleVisible = function() {
        var scenario = this;
        
        if (scenario.visible()) { //make invisible
            scenario.visible(false);
            app.setLayerVisibility(scenario, false);
            
            app.viewModel.removeFromAggregatedAttributes(scenario.name);
            
        } else { //make visible
            scenario.visible(true);
            app.setLayerVisibility(scenario, true);
        }
    };

    // is description active
    self.infoActive = ko.observable(false);
    app.viewModel.showOverview.subscribe( function() {
        if ( app.viewModel.showOverview() === false ) {
            self.infoActive(false);
        }
    });
    
    // display descriptive text below the map
    self.toggleDescription = function(scenario) {
        if ( ! scenario.infoActive() ) {
            self.showDescription(scenario);
        } else {
            self.hideDescription(scenario);
        }
    };
    
    self.showDescription = function(scenario) {
        app.viewModel.showOverview(false);
        app.viewModel.activeInfoSublayer(false);
        app.viewModel.activeInfoLayer(scenario);
        self.infoActive(true);
        $('#overview-overlay').height(186);
        app.viewModel.showOverview(true);
        app.viewModel.updateCustomScrollbar('#overview-overlay-text');
        // app.viewModel.hideMapAttribution();
        app.viewModel.closeAttribution();
    };
    
    self.hideDescription = function(scenario) {
        app.viewModel.showOverview(false);
        app.viewModel.activeInfoSublayer(false);
        app.viewModel.showMapAttribution();
    };
    
    return self;
} // end scenarioModel


function scenariosModel(options) {
    var self = this;
    
    self.scenarioList = ko.observableArray();    
    self.scenarioForm = ko.observable(false);
    
    self.activeSelections = ko.observableArray();
    self.selectionList = ko.observableArray(); 
    self.selectionForm = ko.observable(false);
    
    self.drawingList = ko.observableArray();
    self.drawingForm = ko.observable(false);
    
    self.getSelectionById = function(id) {
        var selections = self.selectionList();
        for (var i=0; i<selections.length; i++) {
            if ( selections[i].id === id ) {
                return selections[i];
            }
        }
        return false;
    };
    
        
    self.reportsVisible = ko.observable(false);
    self.showComparisonReports = function() {
        setTimeout(function() {
            $('#designs-slide').hide('slide', {direction: 'left'}, 300);
        }, 100);
        setTimeout(function() {
            self.reportsVisible(true);
            $('#designs-slide').show('slide', {direction: 'right'}, 300);
            if (self.activeSelections().length > 0) {
                self.reports.noActiveCollections(false);
                app.viewModel.scenarios.reports.updateChart();
            } else { 
                self.reports.noActiveCollections(true);
            }
        }, 420);
    };
    
    self.returnToDesigns = function() {
        setTimeout(function() {
            $('#designs-slide').hide('slide', {direction: 'right'}, 300);
        }, 100);
        setTimeout(function() {
            app.viewModel.scenarios.reportsVisible(false);
            $('#designs-slide').show('slide', {direction: 'left'}, 300);
            self.updateDesignsScrollBar();
        }, 420);
    };
    
    
    self.leaseblockLayer = ko.observable(false);

    self.leaseblockLayer.subscribe( function() {
        app.viewModel.updateAttributeLayers();
    });
    
    self.scenarioLeaseBlocksLayerName = 'Selected OCS Blocks';
        
    // loading message for showing spinner
    // false for normal operation
    self.loadingMessage = ko.observable(false);
    self.errorMessage = ko.observable(false);
    
    self.sharingGroups = ko.observableArray();
    self.hasSharingGroups = ko.observable(false);
    
    self.sharingLayer = ko.observable();
    self.showSharingModal = function(scenario) {
        self.sharingLayer(scenario);
        self.sharingLayer().temporarilySelectedGroups(self.sharingLayer().selectedGroups().slice(0));
        $('#share-modal').modal('show');
    };
    
    self.groupMembers = function(groupName) {
        var memberList = "";
        for (var i=0; i<self.sharingGroups().length; i++) {
            var group = self.sharingGroups()[i];
            if (group.group_name === groupName) {
                for (var m=0; m<group.members.length; m++) {
                    var member = group.members[m];
                    memberList += member + '<br>';
                }
            }
        }
        return memberList;
    };
        
    self.toggleGroup = function(obj) {
        var groupName = obj.group_name,
            indexOf = self.sharingLayer().temporarilySelectedGroups.indexOf(groupName);
        if ( indexOf === -1 ) {  //add group to list
            self.sharingLayer().temporarilySelectedGroups.push(groupName);
        } else { //remove group from list
            self.sharingLayer().temporarilySelectedGroups.splice(indexOf, 1);
        }
    };
    
    self.initSharingModal = function() {
        for (var i=0; i<self.sharingGroups().length; i++) {
            var groupID = '#' + self.sharingGroups()[i].group_slug;
            $(groupID).collapse( { toggle: false } );
        }
    };
    
    //TODO:  Fix the problem in which the first group toggled open will not toggle open again, once it's closed
    self.lastMembersClickTime = 0;
    self.toggleGroupMembers = function(obj, e) {
        var groupName = obj.group_name,
            groupID = '#' + obj.group_slug,
            clickTime = new Date().getTime();
        if (clickTime - self.lastMembersClickTime > 800) {
            self.lastMembersClickTime = clickTime;
            if ( ! $(groupID).hasClass('in') ) {  //toggle on and add group to list
                $(groupID).css("display", "none"); //allows the fade effect to display as expected
                if ( $.browser.msie ) {
                    $(groupID).fadeIn(0, function() {});
                } else {
                    $(groupID).fadeIn('slow', function() {});
                }
                $(groupID).collapse('show'); 
            } else { //toggle off and remove group from list
                if ( $.browser.msie ) {
                    $(groupID).fadeOut(0, function() {});
                } else {
                    $(groupID).fadeOut('slow', function() {});
                }
                $(groupID).collapse('hide');
                //set .modal-body background to eliminate residue that appears when the last Group is opened and then closed?
            }
            setTimeout(function() { self.updateSharingScrollBar(groupID); }, 300);
        }
    };
    
    self.groupIsSelected = function(groupName) {
        if (self.sharingLayer()) {
            var indexOf = self.sharingLayer().temporarilySelectedGroups.indexOf(groupName);
            return indexOf !== -1;
        }
        return false;
    };
    
    self.zoomToScenario = function(scenario) {
        if (scenario.layer) {
            var layer = scenario.layer;
            if (!scenario.active()) {
                scenario.activateLayer();
            }
            app.map.zoomToExtent(layer.getDataExtent());
            if (scenario.uid.indexOf('leaseblockselection') !== -1) {
                app.map.zoomOut();
                app.map.zoomOut();
            } else if (scenario.uid.indexOf('drawing') !== -1) {
                app.map.zoomOut();
                app.map.zoomOut();
            } 
        } else {
            self.addScenarioToMap(scenario, {zoomTo: true});
        }
    };
    
    self.updateSharingScrollBar = function(groupID) {
        var sharingScrollpane = $('#sharing-groups').data('jsp');
        if (sharingScrollpane === undefined) {
            $('#sharing-groups').jScrollPane( {animateScroll: true});
        } else {
            sharingScrollpane.reinitialise();
            var groupPosition = $(groupID).position().top,
                containerPosition = $('#sharing-groups .jspPane').position().top,
                actualPosition = groupPosition + containerPosition;
            //console.log('group position = ' + groupPosition);
            //console.log('container position = ' + containerPosition);
            //console.log('actual position = ' + actualPosition);
            if (actualPosition > 140) {
                //console.log('scroll to ' + (groupPosition-120));
                sharingScrollpane.scrollToY(groupPosition-120);
            } 
            
        }
    };
    
    
    // scenariosLoaded will be set to true after they have been loaded
    self.scenariosLoaded = false;
    self.selectionsLoaded = false;
    
    self.isScenariosOpen = ko.observable(false);
    self.toggleScenariosOpen = function(force) {
        // ensure designs tab is activated
        $('#designsTab').tab('show');
        
        if (force === 'open') {
            self.isScenariosOpen(true);
        } else if (force === 'close') {
            self.isScenariosOpen(false);
        } else {
            if ( self.isScenariosOpen() ) {
                self.isScenariosOpen(false);
            } else {
                self.isScenariosOpen(true);
            }
        }
        self.updateDesignsScrollBar();
    };       
    self.isCollectionsOpen = ko.observable(false);
    self.toggleCollectionsOpen = function(force) {
        // ensure designs tab is activated
        $('#designsTab').tab('show');
        
        if (force === 'open') {
            self.isCollectionsOpen(true);
        } else if (force === 'close') {
            self.isCollectionsOpen(false);
        } else {
            if ( self.isCollectionsOpen() ) {
                self.isCollectionsOpen(false);
            } else {
                self.isCollectionsOpen(true);
            }
        }
        self.updateDesignsScrollBar();
    };           
    self.isDrawingsOpen = ko.observable(false);
    self.toggleDrawingsOpen = function(force) {
        // ensure designs tab is activated
        $('#designsTab').tab('show');
        
        if (force === 'open') {
            self.isDrawingsOpen(true);
        } else if (force === 'close') {
            self.isDrawingsOpen(false);
        } else {
            if ( self.isDrawingsOpen() ) {
                self.isDrawingsOpen(false);
            } else {
                self.isDrawingsOpen(true);
            }
        }
        self.updateDesignsScrollBar();
    };      
    
    self.updateDesignsScrollBar = function() {
        var designsScrollpane = $('#designs-accordion').data('jsp');
        if (designsScrollpane === undefined) {
            $('#designs-accordion').jScrollPane();
        } else {
            designsScrollpane.reinitialise();
        }
    }; 
    
    //restores state of Designs tab to the initial list of designs
    self.reset = function (obj) {
        self.loadingMessage(false);
        self.errorMessage(false);
        
        //clean up scenario form
        if (self.scenarioForm() || self.scenarioFormModel) {
            self.removeScenarioForm();
        }
        
        //clean up selection form
        if (self.selectionForm() || self.selectionFormModel) {
            self.removeSelectionForm(obj);
        }
        
        //clean up drawing form
        if (self.drawingForm() || self.drawingFormModel) {
            self.removeDrawingForm(obj);
        }
        
        //remove the key/value pair from aggregatedAttributes
        app.viewModel.removeFromAggregatedAttributes(self.leaseblockLayer().name);
        app.viewModel.updateAttributeLayers();
        
        self.updateDesignsScrollBar();
    };
        
    self.removeDrawingForm = function(obj) {    
        self.drawingFormModel.cleanUp();
        self.drawingForm(false);
        var drawingForm = document.getElementById('drawing-form');
        $(drawingForm).empty();
        ko.cleanNode(drawingForm);
        //in case of canceled edit
        if ( obj && obj.cancel && self.drawingFormModel.originalDrawing ) {
            self.drawingFormModel.originalDrawing.deactivateLayer();
            self.drawingFormModel.originalDrawing.activateLayer();
        }
        delete self.drawingFormModel;
    };
    
    self.removeSelectionForm = function(obj) {
        self.selectionForm(false);
        var selectionForm = document.getElementById('selection-form');
        $(selectionForm).empty();
        ko.cleanNode(selectionForm); 
        if (self.selectionFormModel.IE) {
            if (self.selectionFormModel.selectedLeaseBlocksLayer) {
                app.map.removeLayer(self.selectionFormModel.selectedLeaseBlocksLayer);
            }
        } else {
            app.map.removeControl(self.selectionFormModel.leaseBlockSelectionLayerClickControl); 
            app.map.removeControl(self.selectionFormModel.leaseBlockSelectionLayerBrushControl); 
            if (self.selectionFormModel.selectedLeaseBlocksLayer) {
                app.map.removeLayer(self.selectionFormModel.selectedLeaseBlocksLayer); 
            }
            if (self.selectionFormModel.leaseBlockSelectionLayer.layer) {
                app.map.removeLayer(self.selectionFormModel.leaseBlockSelectionLayer.layer);   
            }
            if (self.selectionFormModel.navigationControl) {
                self.selectionFormModel.navigationControl.activate();
            }
        }
        if ( ! self.selectionFormModel.leaseBlockLayerWasActive ) {
            if ( self.selectionFormModel.leaseBlockLayer.active() ) {
                self.selectionFormModel.leaseBlockLayer.deactivateLayer();
            }
        }
        if ( (obj && obj.cancel) && self.selectionFormModel.selection && !self.selectionFormModel.selection.active() ) {
            self.selectionFormModel.selection.activateLayer();
        }
        delete self.selectionFormModel;
        app.viewModel.enableFeatureAttribution();
    };
    
    self.removeScenarioForm = function() {
        self.scenarioForm(false);
        var scenarioForm = document.getElementById('scenario-form');
        $(scenarioForm).empty();
        ko.cleanNode(scenarioForm);
        delete self.scenarioFormModel;
        //hide remaining leaseblocks
        if ( self.leaseblockLayer() && app.map.getLayersByName(self.leaseblockLayer().name).length ) {
            app.map.removeLayer(self.leaseblockLayer()); 
        }
    };
    
    self.createWindScenario = function() {
        //hide designs tab by sliding left
        return $.ajax({
            url: '/features/scenario/form/',
            success: function(data) {
                self.scenarioForm(true);
                $('#scenario-form').html(data);
                self.scenarioFormModel = new scenarioFormModel();
                ko.applyBindings(self.scenarioFormModel, document.getElementById('scenario-form'));
                self.scenarioFormModel.updateDesignScrollBar();
                if ( ! self.leaseblockLayer() && app.viewModel.modernBrowser() ) {
                    self.loadLeaseblockLayer();
                }
            },
            error: function (result) { 
                //debugger; 
            }
        });
    };    

    self.createSelectionDesign = function() {
        return $.ajax({
            url: '/features/leaseblockselection/form/',
            success: function(data) {
                self.selectionForm(true);
                $('#selection-form').html(data);
                if ($.browser.msie && $.browser.version < 9) {
                    self.selectionFormModel = new IESelectionFormModel(); 
                } else {
                    self.selectionFormModel = new selectionFormModel(); 
                }
                ko.applyBindings(self.selectionFormModel, document.getElementById('selection-form'));
            },
            error: function (result) { 
                //debugger; 
            }
        });
    };   

    self.createPolygonDesign = function() {
        return $.ajax({
            url: '/features/aoi/form/',
            success: function(data) {
                app.viewModel.scenarios.drawingForm(true);
                $('#drawing-form').html(data);
                app.viewModel.scenarios.drawingFormModel = new polygonFormModel();
                ko.applyBindings(app.viewModel.scenarios.drawingFormModel, document.getElementById('drawing-form'));
                //self.polygonFormModel.updateDesignScrollBar();
            },
            error: function (result) { 
                //debugger; 
            }
        });
    }; 

    self.createLineDesign = function() {};

    self.createPointDesign = function() {};    
    
    //
    self.addScenarioToMap = function(scenario, options) {
        var scenarioId,
            opacity = .8,
            stroke = 1,
            fillColor = "#00A29B",
            strokeColor = "#00827B",
            zoomTo = (options && options.zoomTo) || false;
        
        if ( scenario ) {
            scenarioId = scenario.uid;
            scenario.active(true);
            scenario.visible(true);
        } else {
            scenarioId = options.uid;
        }
        
        var isDrawingModel = false,
            isSelectionModel = false,
            isScenarioModel = false;
        if (scenarioId.indexOf('drawing') !== -1) {
            isDrawingModel = true;
        }
        else if (scenarioId.indexOf('leaseblockselection') !== -1) {
            isSelectionModel = true;
        } else {
            isScenarioModel = true;
        }
        if (self.scenarioFormModel) {
            self.scenarioFormModel.isLeaseblockLayerVisible(false);
        }
        //perhaps much of this is not necessary once a scenario has been added to app.map.layers initially...?
        //(add check for scenario.layer, reset the style and move on?)
        $.ajax( {
            url: '/features/generic-links/links/geojson/' + scenarioId + '/', 
            type: 'GET',
            dataType: 'json',
            success: function(feature) {
                if ( scenario ) {
                    opacity = scenario.opacity();
                    stroke = scenario.opacity();
                } 
                if ( isDrawingModel ) {
                    fillColor = "#C9BE62";
                    strokeColor = "#A99E42";

                    $.ajax( {
                        url: '/drawing/get_geometry_orig/' + scenarioId + '/',
                        type: 'GET',
                        dataType: 'json',
                        success: function(data) {
                            var format = new OpenLayers.Format.WKT(),
                                wkt = data.geometry_orig,
                                feature = format.read(wkt);
                            scenario.geometry_orig = feature;
                        }, 
                        error: function(result) {
                            debugger;
                        }
                    });
                } 
                var layer = new OpenLayers.Layer.Vector(
                    scenarioId,
                    {
                        projection: new OpenLayers.Projection('EPSG:3857'),
                        displayInLayerSwitcher: false,
                        styleMap: new OpenLayers.StyleMap({
                            fillColor: fillColor,
                            fillOpacity: opacity,
                            strokeColor: strokeColor,
                            strokeOpacity: stroke
                        }),     
                        //style: OpenLayers.Feature.Vector.style['default'],
                        scenarioModel: scenario
                    }
                );
                
                layer.addFeatures(new OpenLayers.Format.GeoJSON().read(feature));
                
                if ( scenario ) {
                    //reasigning opacity here, as opacity wasn't 'catching' on state load for scenarios
                    scenario.opacity(opacity);
                    scenario.layer = layer;
                } else { //create new scenario
                    //only do the following if creating a scenario
                    var properties = feature.features[0].properties;
                    if (isDrawingModel) {
                        scenario = new drawingModel({
                            id: properties.uid,
                            uid: properties.uid,
                            name: properties.name, 
                            description: properties.description,
                            features: layer.features
                        });
                        self.toggleDrawingsOpen('open');
                        self.zoomToScenario(scenario);
                    } else if (isSelectionModel) {
                        scenario = new selectionModel({
                            id: properties.uid,
                            uid: properties.uid,
                            name: properties.name, 
                            description: properties.description,
                            features: layer.features
                        });
                        self.toggleCollectionsOpen('open');
                        self.zoomToScenario(scenario);
                    } else {
                        scenario = new scenarioModel({
                            id: properties.uid,
                            uid: properties.uid,
                            name: properties.name, 
                            description: properties.description,
                            features: layer.features
                        });
                        self.toggleScenariosOpen('open');
                        self.zoomToScenario(scenario);
                    }
                    scenario.layer = layer;
                    scenario.layer.scenarioModel = scenario;
                    scenario.active(true);
                    scenario.visible(true);
                    
                    //get attributes
                    $.ajax( {
                        url: '/drawing/get_attributes/' + scenarioId + '/', 
                        type: 'GET',
                        dataType: 'json',
                        success: function(result) {
                            scenario.scenarioAttributes = result.attributes;
                            if (isSelectionModel) {
                                scenario.scenarioReportValues = result.report_values;
                            }
                        },
                        error: function (result) {
                            //debugger;
                        }
                    
                    });
                    
                    //in case of edit, removes previously stored scenario
                    //self.scenarioList.remove(function(item) { return item.uid === scenario.uid } );
                    
                    if ( isDrawingModel ) {
                        var previousDrawing = ko.utils.arrayFirst(self.drawingList(), function(oldDrawing) {
                            return oldDrawing.uid === scenario.uid;
                        });
                        if ( previousDrawing ) {
                            self.drawingList.replace( previousDrawing, scenario );
                        } else {
                            self.drawingList.push(scenario);
                        }
                        self.drawingList.sort(self.alphabetizeByName);
                    } else if ( isSelectionModel ) {
                        var previousSelection = ko.utils.arrayFirst(self.selectionList(), function(oldSelection) {
                            return oldSelection.uid === scenario.uid;
                        });
                        if ( previousSelection ) {
                            self.selectionList.replace( previousSelection, scenario );
                        } else {
                            self.selectionList.push(scenario);
                        }
                        self.activeSelections().push(scenario);
                        self.selectionList.sort(self.alphabetizeByName);
                    } else {
                        var previousScenario = ko.utils.arrayFirst(self.scenarioList(), function(oldScenario) {
                            return oldScenario.uid === scenario.uid;
                        });
                        if ( previousScenario ) {
                            self.scenarioList.replace( previousScenario, scenario );
                        } else {
                            self.scenarioList.push(scenario);
                        }
                        self.scenarioList.sort(self.alphabetizeByName);
                    }
                    
                    //self.scenarioForm(false);
                    self.reset();
                }
                
                //app.addVectorAttribution(layer);
                //in case of edit, removes previously displayed scenario
                for (var i=0; i<app.map.layers.length; i++) {
                    if (app.map.layers[i].name === scenario.uid) {
                        app.map.removeLayer(app.map.layers[i]);
                        i--;
                    }
                }
                app.map.addLayer(scenario.layer); 
                //add scenario to Active tab    
                app.viewModel.activeLayers.remove(function(item) { return item.uid === scenario.uid; } );
                app.viewModel.activeLayers.unshift(scenario);
                
                if (zoomTo) {
                    self.zoomToScenario(scenario);
                }
                
            },
            error: function(result) {
                //debugger;
                app.viewModel.scenarios.errorMessage(result.responseText.split('\n\n')[0]);
            }
        });
    }; // end addScenarioToMap
    
    self.alphabetizeByName = function(a, b) {
        var name1 = a.name.toLowerCase(),
            name2 = b.name.toLowerCase();
        if (name1 < name2) {
            return -1;
        } else if (name1 > name2) {
            return 1;
        }
        return 0;
    };
    
    // activate any lingering designs not shown during loadCompressedState
    self.showUnloadedDesigns = function() {
        var designs = app.viewModel.unloadedDesigns;
        
        if (designs && designs.length) {
            //the following delay might help solve what appears to be a race condition 
            //that prevents the design in the layer list from displaying the checked box icon after loadin
            setTimeout( function() {
                for (var x=0; x < designs.length; x=x+1) {
                    var id = designs[x].id,
                        opacity = designs[x].opacity,
                        isVisible = designs[x].isVisible;
                        
                    if (app.viewModel.layerIndex[id]) {
                        app.viewModel.layerIndex[id].opacity(opacity);
                        app.viewModel.layerIndex[id].activateLayer();
                        for (var i=0; i < app.viewModel.unloadedDesigns.length; i=i+1) {
                            if(app.viewModel.unloadedDesigns[i].id === id) { 
                                app.viewModel.unloadedDesigns.splice(i,1);
                                i = i-1;
                            }
                        }
                    }
                }
            }, 400);
        }
    };
    
    self.loadScenariosFromServer = function() {
        $.ajax({
            url: '/scenario/get_scenarios',
            type: 'GET',
            dataType: 'json',
            success: function (scenarios) {
                self.loadScenarios(scenarios);
                self.scenariosLoaded = true;
                self.showUnloadedDesigns();
            },
            error: function (result) {
                //debugger;
            }
        });
    };
    
    //populates scenarioList
    self.loadScenarios = function (scenarios) {
        self.scenarioList.removeAll();
        $.each(scenarios, function (i, scenario) {
            var scenarioViewModel = new scenarioModel({
                id: scenario.uid,
                uid: scenario.uid,
                name: scenario.name,
                description: scenario.description,
                attributes: scenario.attributes,
                shared: scenario.shared,
                sharedByUsername: scenario.shared_by_username,
                sharedByName: scenario.shared_by_name,
                sharingGroups: scenario.sharing_groups
            });
            self.scenarioList.push(scenarioViewModel);
            app.viewModel.layerIndex[scenario.uid] = scenarioViewModel;
        });
        self.scenarioList.sort(self.alphabetizeByName);
    };
    
    self.loadSelectionsFromServer = function() {
        $.ajax({
            url: '/scenario/get_selections',
            type: 'GET',
            dataType: 'json',
            success: function (selections) {
                self.loadSelections(selections);
                self.selectionsLoaded = true;
                self.showUnloadedDesigns();
            },
            error: function (result) {
                //debugger;
            }
        });
    };
    //populates selectionList
    self.loadSelections = function (selections) {
        self.selectionList.removeAll();
        $.each(selections, function (i, selection) {
            var selectionViewModel = new selectionModel({
                id: selection.uid,
                uid: selection.uid,
                name: selection.name,
                description: selection.description,
                attributes: selection.attributes,
                shared: selection.shared,
                sharedByUsername: selection.shared_by_username,
                sharedByName: selection.shared_by_name,
                sharingGroups: selection.sharing_groups
            });
            self.selectionList.push(selectionViewModel);
            app.viewModel.layerIndex[selection.uid] = selectionViewModel;
        });
        self.selectionList.sort(self.alphabetizeByName);
    };
    
    self.loadDrawingsFromServer = function() {
        $.ajax({
            url: '/drawing/get_drawings',
            type: 'GET',
            dataType: 'json',
            success: function (drawings) {
                self.loadDrawings(drawings);
                self.drawingsLoaded = true;
                self.showUnloadedDesigns();
            },
            error: function (result) {
                //debugger;
            }
        });
    };
    //populates drawingList
    self.loadDrawings = function (drawings) {
        self.drawingList.removeAll();
        $.each(drawings, function (i, drawing) {
            var drawingViewModel = new drawingModel({
                id: drawing.uid,
                uid: drawing.uid,
                name: drawing.name,
                description: drawing.description,
                attributes: drawing.attributes,
                shared: drawing.shared,
                sharedByUsername: drawing.shared_by_username,
                sharedByName: drawing.shared_by_name,
                sharingGroups: drawing.sharing_groups
            });
            self.drawingList.push(drawingViewModel);
            app.viewModel.layerIndex[drawing.uid] = drawingViewModel;
        });
        self.drawingList.sort(self.alphabetizeByName);
    };
    
    self.loadLeaseblockLayer = function() {
        //console.log('loading lease block layer');
        var leaseBlockLayer = new OpenLayers.Layer.Vector(
            self.scenarioLeaseBlocksLayerName,
            {
                projection: new OpenLayers.Projection('EPSG:3857'),
                displayInLayerSwitcher: false,
                strategies: [new OpenLayers.Strategy.Fixed()],
                protocol: new OpenLayers.Protocol.HTTP({
                    //url: '/media/data_manager/geojson/LeaseBlockWindSpeedOnlySimplifiedNoDecimal.json',
                    url: '/media/data_manager/geojson/ofr_planning_grid.json',
                    format: new OpenLayers.Format.GeoJSON()
                }),
                //styleMap: new OpenLayers.StyleMap( { 
                //    "default": new OpenLayers.Style( { display: "none" } )
                //})
                layerModel: new layerModel({
                    name: self.scenarioLeaseBlocksLayerName
                })
            }
        );
        self.leaseblockLayer(leaseBlockLayer);
        
        self.leaseblockLayer().events.register("loadend", self.leaseblockLayer(), function() {
            if (self.scenarioFormModel && ! self.scenarioFormModel.IE) {
                self.scenarioFormModel.showLeaseblockSpinner(false);
            }
        });
    };      
    
    self.leaseblockList = [];    
    
    //populates leaseblockList
    self.loadLeaseblocks = function (ocsblocks) {
        self.leaseblockList = ocsblocks;
    };  
    
    self.cancelShare = function() {
        self.sharingLayer().temporarilySelectedGroups.removeAll();
    };
    
    //SHARING DESIGNS
    self.submitShare = function() {
        self.sharingLayer().selectedGroups(self.sharingLayer().temporarilySelectedGroups().slice(0));
        var data = { 'scenario': self.sharingLayer().uid, 'groups': self.sharingLayer().selectedGroups() };
        $.ajax( {
            url: '/scenario/share_design',
            data: data,
            type: 'POST',
            dataType: 'json',
            error: function(result) {
                //debugger;
            }
        });
    };
    
    return self;
} // end scenariosModel


app.viewModel.scenarios = new scenariosModel();

$('#designsTab').on('show', function (e) {
    //if ( app.viewModel.scenarios.reports && app.viewModel.scenarios.reports.showingReport() ) {
    //    app.viewModel.scenarios.reports.updateChart();
    //}
    // if ( !app.viewModel.scenarios.scenariosLoaded || !app.viewModel.scenarios.selectionsLoaded) {
    if ( !app.viewModel.scenarios.drawingsLoaded ) {
        // load the scenarios
        app.viewModel.scenarios.loadScenariosFromServer();
        
        // load the selections
        // app.viewModel.scenarios.loadSelectionsFromServer();

        // load the drawing
        app.viewModel.scenarios.loadDrawingsFromServer();
        
        // load the leaseblocks
        // $.ajax({
        //     url: '/scenario/get_leaseblocks',
        //     type: 'GET',
        //     dataType: 'json',
        //     success: function (ocsblocks) {
        //         app.viewModel.scenarios.loadLeaseblocks(ocsblocks);
        //     },
        //     error: function (result) {
        //         //debugger;
        //     }
        // });
        
        $.ajax({
            url: '/scenario/get_sharing_groups',
            type: 'GET',
            dataType: 'json',
            success: function (groups) {
                app.viewModel.scenarios.sharingGroups(groups);
                if (groups.length) {
                    app.viewModel.scenarios.hasSharingGroups(true);
                }
            },
            error: function (result) {
                //debugger;
            }
        });
    }
});