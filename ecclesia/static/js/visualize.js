Node = function (config) {
	this.config = {
		dimensions	: {},
		id			: -1,
		url			: '',
		name		: ''
	};
    this.state = {
        hover   : false,
        drag    : false
    };
	$.extend(true, this.config, config || {});
};
Node.prototype = {
	toString	: function () {
		return this.config.name;
	},
	serialize	: function () {
		return $.param(this.config.dimensions) + '&pk=' + this.config.id;
	},
	loadImage	: function () {
		// setting the background image and making sure the image is loaded
		if(this.config.bg_image && this.config.bg_src) {
			this.config.bg_image.src = this.config.bg_src;
		}
	},
    wrapTitle   : function (container) {
        var container_w = container.width();
        var title_padding = parseInt(container.children('a').css('padding-right'))
                            + parseInt(container.children('a').css('padding-left'));
        container.children('a').width(container_w - title_padding - 2);
    },
    roundedRect	: function (ctx,x,y,width,height,radius,fill_color,stroke_color){
		ctx.save();
		// init the colors
		ctx.fillStyle = fill_color;
		ctx.strokeStyle = stroke_color;
		// create the image
		ctx.beginPath();
		ctx.moveTo(x,y+radius);
		ctx.lineTo(x,y+height-radius);
		ctx.quadraticCurveTo(x,y+height,x+radius,y+height);
		ctx.lineTo(x+width-radius,y+height);
		ctx.quadraticCurveTo(x+width,y+height,x+width,y+height-radius);
		ctx.lineTo(x+width,y+radius);
		ctx.quadraticCurveTo(x+width,y,x+width-radius,y);
		ctx.lineTo(x+radius,y);
		ctx.quadraticCurveTo(x,y,x,y+radius);
		ctx.fill();
		ctx.stroke();
		// restore former context options
		ctx.restore();
    }
};

Group = function (node_class, config) {
	this.config = {
		alias		: 'group',
		model_name	: 'GroupProfile',
		bg_src		: '/static/img/cork_board.jpg',
		bg_image	: new Image()
	};
	// inheriting Node class
	var dummy = $.extend(true, node_class, this);
	$.extend(true, this, dummy);
	// reconfig
	$.extend(this.config, config || {});
	this.loadImage();
};
Group.prototype = {
	serialize	: function () {
		return $.param(this.config.dimensions) + '&model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	addToDOM	: function (container) {
		var c = this.config;
		$('#'+container).append('<div class="'+c.alias+'" id="'+c.alias+'_'+c.id+'"><a href="'+c.url+'" class="'+c.alias+'_title">'+c.name+'</a></div>');
	},
	position	: function () {
		var c = this.config;
		var id_selector = '#'+c.alias+'_'+c.id;
		$(id_selector).css('left', c.dimensions.x+'px');
		$(id_selector).css('top', c.dimensions.y+'px');
	},
	draw		: function (ctx) {
		var dims = this.config.dimensions;
		if(this.config.bg_image) {
			try {
				ctx.drawImage(this.config.bg_image, dims.x, dims.y, dims.w, dims.h);
			} catch(e){}
			ctx.strokeRect(dims.x, dims.y, dims.w, dims.h);
		}
	}
};

Discussion = function (node_class, config) {
	this.config = {
		alias		: 'disc',
		model_name	: 'Discussion',
		bg_src		: '/static/img/whiteboard.jpg',
		bg_image	: new Image()
	};
	// inheriting Node class
	var dummy = $.extend(true, node_class, this);
	$.extend(true, this, dummy);
	// reconfig
	$.extend(this.config, config || {});
	this.loadImage();
};
Discussion.prototype = {
	serialize	: function () {
		return $.param(this.config.dimensions) + '&model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	addToDOM	: function (container) {
		var c = this.config;
		$('#'+container).append('<div class="'+c.alias+'" id="'+c.alias+'_'+c.id+'"><a href="'+c.url+'" class="'+c.alias+'_title">'+c.name+'</a></div>');
	},
	position	: function () {
		var c = this.config;
		var id_selector = '#'+c.alias+'_'+c.id;
		$(id_selector).css('left', c.dimensions.x+'px');
		$(id_selector).css('top', c.dimensions.y+'px');
	},
	draw		: function (ctx) {
		var dims = this.config.dimensions;
		if(this.config.bg_image) {
			try {
				ctx.drawImage(this.config.bg_image, dims.x, dims.y, dims.w, dims.h);
			} catch(e){}
		}
	}
};

Story = function (node_class, config) {
	this.config = {
		alias	    	: 'story',
		model_name  	: 'Story',
		type	    	: 'goal',
        fill_normal     : '#e3e3e3',
        fill_hover      : '#f2f2f2',
        stroke_normal   : '#444',
        stroke_hover    : '#000'
	};
	// inheriting Node class
	var dummy = $.extend(true, node_class, this);
	$.extend(true, this, dummy);
	// reconfig
	$.extend(this.config, config || {});
    // set the id that connects this instance to the DOM
    this.DOMid = this.config.alias+'_'+this.config.id;
};
Story.prototype = {
	serialize	: function () {
		return $.param(this.config.dimensions) + '&model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	addToDOM	: function () {
		var c = this.config;
		$('#'+c.type+'_container').append('<div class="'+c.alias+'" id="'+this.DOMid+'"><a href="'+c.url+'" class="'+c.alias+'_title">'+c.name+'</a></div>');
		this.wrapTitle($('#'+this.DOMid));
	},
	position	: function () {
		var c = this.config;
		var id_selector = '#'+this.DOMid
		$(id_selector).css('left', c.dimensions.x+'px');
		$(id_selector).css('top', c.dimensions.y+'px');
	},
	draw		: function (ctx) {
		var dims = this.config.dimensions;
        var state = this.state.hover ? 'hover' : 'normal';
		this.roundedRect(ctx, dims.x, dims.y, dims.w, dims.h, 5, this.config['fill_'+state], this.config['stroke_'+state]);
	},
    hover       : function (ctx) {
        this.state.hover = true;
        this.draw(ctx);
        //$('#'+this.DOMid).children('.opinions').show();
    },
    unhover     : function (ctx) {
        this.state.hover = false;
        this.draw(ctx);
        //$('#'+this.DOMid).children('.opinions').hide();
    }
};
Relation = function (node_class, config) {
	this.config = {
		alias		: 'relation',
		model_name	: 'StoryRelation',
		from_id		: -1,
		to_id		: -1,
		from		: {},
		to			: {}
	};
	// inheriting Node class
	var dummy = $.extend(true, node_class, this);
	$.extend(true, this, dummy);
	// reconfig
	$.extend(this.config, config || {});
};
Relation.prototype = {
	serialize	: function () {
		return 'model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	toString	: function () {
		return "("+this.from.toString()+","+this.to.toString()+")";
    },
	bezier		: function (ctx,x1,y1,x2,y2,label) {
		ctx.save();
		ctx.beginPath();
		ctx.lineWidth = 2;
		ctx.strokeStyle="rgb(130,130,200)";
		ctx.moveTo(x1,y1);
		ctx.bezierCurveTo(x1+(x2-x1)/2,y1,x2-(x2-x1)/2,y2,x2,y2);
		ctx.stroke();
		//drawText(label,(x1+x2)/2, (y1+y2)/2, x2-x1,Math.atan2(y2-y1,x2-x1));
		ctx.restore();
    },
	addToDOM	: function (container) {
		var c = this.config;
		$('#'+container).append('<div class="'+c.alias+'" id="'+c.alias+'_'+c.id+'"><a href="'+c.url+'" class="'+c.alias+'_title">'+c.name+'</a></div>');
	},
	draw		: function (ctx) {
		// get the dimensions of the from and to elements
		var from_dims = this.config.from.config.dimensions;
		var to_dims = this.config.to.config.dimensions;
		// calculate the from and to points
		var x1 = from_dims.x + from_dims.w;
		var y1 = from_dims.y + from_dims.h/2;
		var x2 = to_dims.x
		var y2 = to_dims.y + to_dims.h/2;
		// draw it
		this.bezier(ctx, x1, y1, x2, y2);
	}
};
Opinion = function (node_class, config) {
	this.config = {
		alias		: 'opinion',
		model_name	: 'Opinion',
		type		: 'for',
		parent_id	: -1,
		parent		: {},
		container_id: '',
		added		: false
	};
	// inheriting Node class
	var dummy = $.extend(true, node_class, this);
	$.extend(true, this, dummy);
	// reconfig
	$.extend(this.config, config || {});
};
Opinion.prototype = {
	serialize	: function () {
		return 'model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	addToDOM	: function () {
		var c = this.config;
		$('#'+c.container_id).append('<div class="'+c.alias+'" id="'+c.alias+'_'+c.id+'"></div>');
	},
	container	: function () {
		if(this.config.parent.config) {
			var c = this.config;
			var pc = c.parent.config;
			c.container_id = pc.alias+'_'+pc.id+'_'+c.type;
			// try getting the container from the DOM
			var id_selector = '#'+c.container_id;
			var container = $(id_selector);
			// check if it exists and return it if it does
			if(container.length) { return this; }
			// if it doesn't we create it
            var parent_dims = pc.dimensions;
			var margin = 3;
			var opn_edge = 24;
			var x,y;
			$('#'+pc.alias+'_'+pc.id).append('<div class="opinions '+c.type+'_opinions" id="'+c.container_id+'"><canvas width="'+opn_edge+'" height="'+opn_edge+'" id="'+c.container_id+'_bg" class="opinion_container_bg"></canvas><a href="#"></a></div>');
			// position the container and set its style
			switch(c.type) {
				case 'good': {
					x = parent_dims.w - opn_edge;
					y = - (opn_edge);
				} break;
				case 'bad': {
					x = parent_dims.w - opn_edge*2 -2; //adding 2 for borders
					y = - (opn_edge);
				} break;
				case 'true': {
					x = parent_dims.w - opn_edge*3 -4;
					y = - (opn_edge);
				} break;
				case 'false': {
					x = parent_dims.w - opn_edge*4 -6;
					y = - (opn_edge);
				} break;
			}
			$(id_selector).css('left', x+'px')
			              .css('top', y+'px');
            // draw its background
            this.drawContainerBg(c.container_id);
			return this;
		} else {
			throw new Error('No parent element is set for: '+c.id);
		}
	},
	position	: function () {},
	draw		    : function () {
        if(!this.config.added) {
			var opns = parseInt($('a', '#'+this.config.container_id).text());
			if(!opns) { opns = 1; }
				 else { opns += 1; }
			$('a', '#'+this.config.container_id).text(opns);
			this.config.added = true;
		}
	},
    drawContainerBg : function (container_id) {
        var id = container_id+'_bg';
        var ctx = $('#'+id).get(0).getContext('2d');
        var w = $('#'+container_id).innerWidth();
        var h = $('#'+container_id).innerHeight();
        var color = '#eee';
        switch(container_id.split('_')[2]) {
            case 'good': color = '#cfc'; break;
            case 'bad': color = '#fcc'; break;
            case 'true': color = '#ccf'; break;
            case 'false': color = '#ffc'; break;
        }
        if(ctx) {
            this.roundedRect(ctx, 0, 0, w, h, 8, color, '#666');
        }
    }
};

VUController = function (options) {
	_VUC = this;
    this.options = {
		width		: 958,
		height		: 600,
		container_id: 'canvasContainer',
		canvas_id	: 'groupsvu',
		data_url	: '/get_groups_view_json/',
		update_url	: '/common/update_presentation/',
		meta_url	: ''
	};
	$.extend(this.options, options || {});
	
	this.data = {};
	this.elems = {};
	this.drag = {};
	this.ctx = null;
};
VUController.prototype = {
	setElementsRelations: function () {
		//var _VUC = this;
		$.each(_VUC.elems, function (key, el) {
			var c = _VUC.elems[key].config;
			if(el instanceof Relation) {
				c.from = _VUC.elems[c.from_id];
				c.to = _VUC.elems[c.to_id];
			} else if(el instanceof Opinion) {
				c.parent = _VUC.elems[c.parent_id];
			}
		});
	},
	createNodes			: function () {
		//var _VUC = this;
		$.each(_VUC.data, function (i, item) {
			$.each(item, function (key, val) {
				var node = new Node({});
				switch(key) {
					case 'group':
						node = new Group(node, val);
						break;
					case 'discussion':
						node = new Discussion(node, val);
						break;
					case 'story':
						node = new Story(node, val);
						break;
					case 'relation':
						node = new Relation(node, val);
						break;
					case 'opinion':
						node = new Opinion(node, val);
						break;
				}
				var id = node.config.alias+'_'+node.config.id;
				// add the Node instance to the controller's elements
				_VUC.elems[id] = node;
				// set a load event listener to the element's background image to initialy draw it
				if(node.config.bg_image) {
					$(node.config.bg_image).load(function () {
						node.draw(_VUC.ctx);
					});
				}
			});
		});
		_VUC.setElementsRelations();
	},
	initCanvas			: function () {
		var o = _VUC.options;
		$('#'+o.container_id).empty();
		$('#'+o.container_id).append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		_VUC.ctx = document.getElementById(o.canvas_id).getContext('2d');
		return (_VUC.ctx);
	},
	setDraggable		: function (el) {
		//var _VUC = this;
		// set a specific element as draggable
		if(el) {
			var id = el.config.alias+'_'+el.config.id;
			$('#'+id).draggable({
				containment: 'parent',
				start: function (e, ui) {
					_VUC.elems[id].state.drag = true;
                    _VUC.setDrag(id);
					_VUC.grip();
				},
				stop : function (e, ui) {
					var position = $(this).position();
					var el = _VUC.elems[id];
                    el.state.drag = false;
                    el.config.dimensions.x = parseInt(position.left);
					el.config.dimensions.y = parseInt(position.top);
					_VUC.drop();
				}
			});
		}
		// set all elements as draggable
		else {
			$.each(_VUC.elems, function (id, el) {
				_VUC.setDraggable(el);
			});
		}
	},
    setEventHandlers    : function (el) {
        if(el) {
            //var _VUC = this;
            if(el.hover && $.isFunction(el.hover)) {
                $('#'+el.DOMid).hover(
                    function () {
                        if(el.state.drag) { return; }
                        else { el.hover(_VUC.ctx); }
                    },
                    function () {
                        if(el.state.drag) { return; }
                        else { el.unhover(_VUC.ctx); }
                    }
                );
            }
        }
    },
	addElement			: function (el) {
		// add an element to the DOM
		if(el) {
			el.addToDOM(_VUC.options.container_id);
		}
		// add all elements to the DOM
		else {
			//var _VUC = this;
			$.each(_VUC.elems, function (id, el) {
				_VUC.addElement(el);
			});
		}
	},
	getData				: function () {
		//var _VUC = this;
		// expecting format: [ { element_alias : { element_config_object }, ... ]
		$.getJSON(_VUC.options.data_url, function (data){
			_VUC.data = data;
			// initialize the view controller
			_VUC.init(true);
		});
	},
	init				: function (loaded) {
		if(!loaded || loaded === 'reload') {
			// get the data
			_VUC.getData();
		} else {
			// create the elements
			_VUC.createNodes();
			// initialize the canvas
			if(_VUC.initCanvas()) {
				//var _VUC = this;
				// iterate over the elements and create the GUI
				$.each(_VUC.elems, function (id, el) {
					// appending a div for each element to the canvas container
					_VUC.addElement(el);
					// position the element inside the container
					_VUC.position(el);
					// set it as draggable
					_VUC.setDraggable(el);
                    // set other event handlers
                    _VUC.setEventHandlers(el);
				});
				// we have initialized the canvas so draw the element
				_VUC.draw();
			} else {
				alert('No canvas context.');
			}
		}
	},
	position			: function (el) {
		if(el.position) {
			el.position();
		}
	},
	setDrag				: function (id) {
		_VUC.drag = _VUC.elems[id];
	},
	draw				: function (isGrip) {
		//var _VUC = this;
		_VUC.ctx.clearRect(0, 0, _VUC.options.width, _VUC.options.height);
		$.each(_VUC.elems, function (id, el) {
			if(isGrip) {
				if(id != _VUC.drag.config.alias+'_'+_VUC.drag.config.id) {
					el.draw(_VUC.ctx);
				}
			} else {
				el.draw(_VUC.ctx);
			}
		});
	},
	grip				: function () {
		$('#'+_VUC.drag.config.alias+'_'+_VUC.drag.config.id).addClass('dragon');
		_VUC.draw(true);
	},
	drop				: function () {
		$('#'+_VUC.drag.config.alias+'_'+_VUC.drag.config.id).removeClass('dragon');
		_VUC.draw();
		_VUC.updatePresentation();
	},
	updatePresentation	: function () {
		//var _VUC = this;
		/*$.each(this.elems, function (id, el){
			_VUC.data[id] = el.serialize();
		});*/
		_VUC.data = _VUC.drag.serialize();
		
		$.ajax({
			type		: "POST",
			url			: _VUC.options.update_url,
			data		: _VUC.data,
			success		: function (msg){
				//alert(msg);
			}
		});
	}
};
/*
 *	A controller class that handles Discussions GUI.
 *	Accepts a VUController object instance and inherits it
 *	using jQuery.extend()
 *  ( sort of an inheritance :P )
 */
DiscussionController = function (VuController, options) {
	_VUC = this;
    this.options = {};
	// inheriting Node class
	var dummy = $.extend(true, VuController, this);
	$.extend(true, this, dummy);
	// set the options
	$.extend(this.options, options || {});

    this.metaData = {};
};
DiscussionController.prototype = {
    getData				: function () {
		//var _DiscC = this;
		// expecting format: [ { element_alias : { element_config_object }, ... ]
		$.getJSON(_VUC.options.data_url, function (data){
			_VUC.data = data;
			// get the Visualization's meta data
			_VUC.getVisualizationMetaData();
		});
	},
	getVisualizationMetaData: function () {
		//var _DiscC = this;
		$.getJSON(_VUC.options.meta_url, function (json) {
            // apply the received data
            _VUC.metaData = json;
            // initialize the view controller
            _VUC.init(true);
		});
	},
    initVisualization   : function () {
        //var _DiscC = this;
        // setting the speech act containers
        $.each(_VUC.metaData, function (i, item) {
            switch(item.fields.story_type) {
                case 1: { // story
                    $('#'+_VUC.options.container_id).append('<div id="'+item.fields.name+'_container" class="stories_container"></div>');
                    $('#'+item.fields.name+'_container').append('<h2>'+item.fields.name+'</h2>');
                } break;
                case 2: { // opinion
                } break;
                case 3: { // relation
                } break;
            }
        });
        // set some style options
        //$('#'+_VUC.options.container_id).css('position', 'relative');
        $('.stories_container').height(_VUC.options.height)
                               .width(_VUC.options.width * 0.25 - 1);
    },
	initCanvas			: function () {
		var o = _VUC.options;
		$('#'+o.container_id).empty()
                             .append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		_VUC.ctx = document.getElementById(o.canvas_id).getContext('2d');
        if(_VUC.metaData.length != 0) {
            _VUC.initVisualization();
        }
		return (_VUC.ctx);
	},
	addElement			: function (el) {
		// add an element to the DOM
		if(el) {
			if(el instanceof Opinion) { el.container().addToDOM(); }
								 else { el.addToDOM(_VUC.options.container_id); }
		}
		// add all elements to the DOM
		else {
			//var _DiscC = this;
			$.each(_VUC.elems, function (id, el) {
				_VUC.addElement(el);
			});
		}
	},
	drawText			: function (text,x,y,maxWidth,rotation) {
    // if text is short enough - put it in 1 line. if not, search for the middle space, and split it there (only splits to 2 lines).
        _VUC.ctx.translate(x,y);
        _VUC.ctx.save();
        _VUC.ctx.rotate(rotation);
        if (_VUC.ctx.measureText(text).width <= maxWidth*0.8){
            _VUC.ctx.fillText(text,0,0);
        } else {
            var spl = text.split('-');
            var len = Math.floor(spl.length/2);
            var pos = 0;
            for (var i=0; i<len; i++){
                pos = text.indexOf('-',pos)+1;
            }            
            var text1 = text.substring(0,pos);
            var text2 = text.substring(pos);
            _VUC.ctx.fillText(text1,0,-10);
            _VUC.ctx.fillText(text2,0,+10);
        }
        _VUC.ctx.restore();
        _VUC.ctx.translate(-x,-y);
    }
};

/*
 *  Class FormController
 *
 * Note on Validation :
 *
 * Each field that should be validated will be
 * added a class with the value of the name of
 * the requested validation function.break
 * e.g.:
 * this input:
 * <input type="text" class="is_value" />
 * will be checked that it is not empty.
 */
FormController = function() {
	this.f_html		= null;
	this.f_jq		= null;
	this.options	= {};
	this.elements	= {};
};
FormController.prototype = {
	/**
	 * gets an object that maps form name to a config object
	 * iterates over the object and adds the submit event
	 * listener to every form
	 * @param Object configs : a map of { name : config }
	 * @return
	 */
	bind				: function (configs) {
		var this_ = this;
		$.each(configs, function(name, config){
			$(document.forms[name]).find(':button[type=submit],:input[type=submit]').bind('click', function(e){
				if($(e.target).attr('name').length && $(e.target).attr('name') == 'action') {
					$.extend(config, { action : $(e.target).val() });
				};
				return this_.submit(this.form, config);
			});
		});
	},
	init				: function (form, options) {
		this.f_html		= form || {};
		this.f_jq		= $(form) || {};
		this.options	= $.extend(true, {
	        validation	: {},
			url			: this.f_jq.attr('action') || '/',
	        type		: this.f_jq.attr('method') || 'POST',
	        dont_post	: false,
	        data_type	: 'text',
	        editor		: {}
	    }, options || {});
		/* for YUI Rich Text Editor
		if(this.options.editor && this.options.editor.saveHTML) {
			this.options.editor.saveHTML();
		}*/
		this.elements = {};
		if(this.f_html.elements) {
			var this_ = this;
			$.each(this.f_html.elements, function (i, el) {
				if($(el).attr('name')) {
					this_.elements[$(el).attr('name')] = el;
				}
			});
		}
	},
	validate			: function () {
		var valid = true;
		this.extractValidation();
		if(this.options.validation && typeof this.options.validation != 'undefined') {
			var this_ = this;
			$.each(this.options.validation, function(field, method){
				// first check that there's a field with this name and that it's not disabled
				if(this_.elements[field] != null && !this_.elements[field].disabled) {
					try {
						if(this_[method] && $.isFunction(this_[method])) {
							if(!this_[method](field)) {
								this_.alert_field(field);
								valid = false;
							} else {
								this_.clear_alert(field);
							}
						}
					} catch(e){alert(e);}
				} else if(this_.elements[field+'[]'] != null && !this_.elements[field+'[]'].disabled) {
					try {
						/*
						 * in case there's a specification for a validation of checkboxes
						 * run an 'OR' test to verify that at least one is checked
						 */
						var _checked = false;
						$.each(this_.elements[field+'[]'], function(index, box){
							_checked = _checked || box.checked;
						});
						valid = _checked;
					} catch(e){alert(e);}
				}
			});
		} else {
			valid = false;
			throw new Error("Form's validation map is missing.");
		}
		return valid;
	},
	/**
	 * the function that is called on the onsubmit event fire
	 * of the form object
	 * @return Boolean false : !! must return false to prevent from redirect to the action url
	 */
	submit				: function (form, options) {
		this.init(form, options);
		if(this.validate()) {
			if(this.before()) {
				if(this.options.dont_post) {
					this.after(this.f_jq.serialize());
				} else {
					this.send();
				}
			}
		}
		return false;
	},
	/**
	 * handles the ajax request
	 * @return Object response : the server's response
	 */
	send				: function () {
		var this_ = this;
		$.ajax({
			type	: this_.options.type,
			url		: this_.options.url,
			data	: this_.f_jq.serialize(),
			dataType: this_.options.data_type,
			success	: function(response){
				this_.after(response);
			}
		});
	},
	/**
	 * a handler for pre ajax request logic
	 * @return Boolean continue : whether to continue to send
	 */
	before				: function () {
		// enable catching form's multiple submit and passing it to send
		if(this.options.action != null && this.options.action != '') {
			this.options.url = this.options.url + this.options.action;
		}
		return true;
	},
	/**
	 * a handler for ajax response logic and calling callbacks
	 * @return Object
	 */
	after				: function (response) {
		if(this.options.callback && typeof this.options.callback == 'function') {
			this.options.callback(response);
		} else {
			alert(response);
		}
	},
	extractValidation	: function () {
		var additional_validation = {};
		$.each(this.elements, function (el_name, el) {
			// disabled fields are not counted
			if(!el.disabled) {
				var classes = $(el).attr('class').split(' ');
				$.each(classes, function(i, _class) {
					// allowing one check per field
					if(_class && _class.indexOf('is_') === 0) {
						additional_validation[el_name] = _class;
					}
				});
			}
		});
		$.extend(this.options.validation, additional_validation);
	},
	alert_field			: function (el_name) {
		$(this.elements[el_name]).addClass('field_alert');
	},
	clear_alert			: function (el_name) {
		$(this.elements[el_name]).removeClass('field_alert');
	},
	/*
	 * validation functions :
	 */
	is_value			: function (el_name) {
		var val = $(this.elements[el_name]).val();
		return val && $.trim(val) != '' && typeof val != 'undefined';
	},
	is_alpha			: function (el_name) {
		return this._validate($(this.elements[el_name]), /[^a-zA-Z\s_-]/g);
	},
	is_numeric			: function (el_name) {
		return this._validate($(this.elements[el_name]), /[\D]/g);
	},
	is_alphanumeric		: function (el_name) {
		return this._validate($(this.elements[el_name]), /[^\w\s-]/g);
	},
	_validate			: function (el, pat ){
		return this.is_value(el.attr('name')) ? !pat.test(el.val()) : false;
	}
};