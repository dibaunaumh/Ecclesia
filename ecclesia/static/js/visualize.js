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
        $('#'+this.DOMid).children('.opinions').show();
    },
    unhover     : function (ctx) {
        this.state.hover = false;
        this.draw(ctx);
        $('#'+this.DOMid).children('.opinions').hide();
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
			$('#'+pc.alias+'_'+pc.id).append('<div class="opinions '+c.type+'_opinions" id="'+c.container_id+'"><canvas id="'+c.container_id+'_bg" class="opinion_container_bg"></canvas><a href="#"></a></div>');
			// position the container and set its style
			var parent_dims = pc.dimensions;
			var margin = 3;
			var opn_edge = 24;
			var x,y;
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
            this.roundedRect(ctx, 0, 0, w, h, 3, color, '#666');
        }
    }
};

VUController = function (options) {
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
		var this_ = this;
		$.each(this.elems, function (key, el) {
			var c = this_.elems[key].config;
			if(el instanceof Relation) {
				c.from = this_.elems[c.from_id];
				c.to = this_.elems[c.to_id];
			} else if(el instanceof Opinion) {
				c.parent = this_.elems[c.parent_id];
			}
		});
	},
	createNodes			: function () {
		var this_ = this;
		$.each(this.data, function (i, item) {
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
				this_.elems[id] = node;
				// set a load event listener to the element's background image to initialy draw it
				if(node.config.bg_image) {
					$(node.config.bg_image).load(function () {
						node.draw(this_.ctx);
					});
				}
			});
		});
		this.setElementsRelations();
	},
	initCanvas			: function () {
		var o = this.options;
		$('#'+o.container_id).empty();
		$('#'+o.container_id).append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		this.ctx = document.getElementById(o.canvas_id).getContext('2d');
		return (this.ctx !== null);
	},
	setDraggable		: function (el) {
		var this_ = this;
		// set a specific element as draggable
		if(el) {
			var id = el.config.alias+'_'+el.config.id;
			$('#'+id).draggable({
				containment: 'parent',
				start: function (e, ui) {
					this_.elems[id].state.drag = true;
                    this_.setDrag(id);
					this_.grip();
				},
				stop : function (e, ui) {
					var position = $(this).position();
					var el = this_.elems[id];
                    el.state.drag = false;
                    el.config.dimensions.x = parseInt(position.left);
					el.config.dimensions.y = parseInt(position.top);
					this_.drop();
				}
			});
		}
		// set all elements as draggable
		else {
			$.each(this.elems, function (id, el) {
				this_.setDraggable(el);
			});
		}
	},
    setEventHandlers    : function (el) {
        if(el) {
            var this_ = this;
            if(el.hover && $.isFunction(el.hover)) {
                $('#'+el.DOMid).hover(
                    function () {
                        if(el.state.drag) { return; }
                        else { el.hover(this_.ctx); }
                    },
                    function () {
                        if(el.state.drag) { return; }
                        else { el.unhover(this_.ctx); }
                    }
                );
            }
        }
    },
	addElement			: function (el) {
		// add an element to the DOM
		if(el) {
			el.addToDOM(this.options.container_id);
		}
		// add all elements to the DOM
		else {
			var this_ = this;
			$.each(this.elems, function (id, el) {
				this_.addElement(el);
			});
		}
	},
	getData				: function () {
		var this_ = this;
		// expecting format: [ { element_alias : { element_config_object }, ... ]
		$.getJSON(this.options.data_url, function (data){
			this_.data = data;
			// initialize the view controller
			this_.init(true);
		});
	},
	init				: function (loaded) {
		if(!loaded) {
			// get the data
			this.getData();
		} else {
			// create the elements
			this.createNodes();
			// initialize the canvas
			if(this.initCanvas()) {
				var this_ = this;
				// iterate over the elements and create the GUI
				$.each(this.elems, function (id, el) {
					// appending a div for each element to the canvas container
					this_.addElement(el);
					// position the element inside the container
					this_.position(el);
					// set it as draggable
					this_.setDraggable(el);
                    // set other event handlers
                    this_.setEventHandlers(el);
				});
				// we have initialized the canvas so draw the element
				this.draw();
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
		this.drag = this.elems[id];
	},
	draw				: function (isGrip) {
		var this_ = this;
		this.ctx.clearRect(0, 0, this.options.width, this.options.height);
		$.each(this.elems, function (id, el) {
			if(isGrip) {
				if(id != this_.drag.config.alias+'_'+this_.drag.config.id) {
					el.draw(this_.ctx);
				}
			} else {
				el.draw(this_.ctx);
			}
		});
	},
	grip				: function () {
		$('#'+this.drag.config.alias+'_'+this.drag.config.id).addClass('dragon');
		this.draw(true);
	},
	drop				: function () {
		$('#'+this.drag.config.alias+'_'+this.drag.config.id).removeClass('dragon');
		this.draw();
		this.updatePresentation();
	},
	updatePresentation	: function () {
		var this_ = this;
		/*$.each(this.elems, function (id, el){
			this_.data[id] = el.serialize();
		});*/
		this.data = this.drag.serialize();
		
		$.ajax({
			type		: "POST",
			url			: this_.options.update_url,
			data		: this_.data,
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
		var this_ = this;
		// expecting format: [ { element_alias : { element_config_object }, ... ]
		$.getJSON(this.options.data_url, function (data){
			this_.data = data;
			// get the Visualization's meta data
			this_.getVisualizationMetaData();
		});
	},
	getVisualizationMetaData: function () {
		var this_ = this;
		$.getJSON(this.options.meta_url, function (json) {
            // apply the received data
            this_.metaData = json;
            // initialize the view controller
            this_.init(true);
		});
	},
    initVisualization   : function () {
        var this_ = this;
        // setting the speech act containers
        $.each(this.metaData, function (i, item) {
            switch(item.fields.story_type) {
                case 1: { // story
                    $('#'+this_.options.container_id).append('<div id="'+item.fields.name+'_container" class="stories_container"></div>');
                    $('#'+item.fields.name+'_container').append('<h2>'+item.fields.name+'</h2>');
                } break;
                case 2: { // opinion
                } break;
                case 3: { // relation
                } break;
            }
        });
        // set some style options
        //$('#'+this_.options.container_id).css('position', 'relative');
        $('.stories_container').height(this_.options.height)
                               .width(this_.options.width * 0.25 - 1);
    },
	initCanvas			: function () {
		var o = this.options;
		$('#'+o.container_id).empty()
                             .append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		this.ctx = document.getElementById(o.canvas_id).getContext('2d');
        if(this.metaData.length != 0) {
            this.initVisualization();
        }
		return (this.ctx !== null);
	},
	addElement			: function (el) {
		// add an element to the DOM
		if(el) {
			if(el instanceof Opinion) { el.container().addToDOM(); }
								 else { el.addToDOM(this.options.container_id); }
		}
		// add all elements to the DOM
		else {
			var this_ = this;
			$.each(this.elems, function (id, el) {
				this_.addElement(el);
			});
		}
	},
	drawText			: function (text,x,y,maxWidth,rotation) {
    // if text is short enough - put it in 1 line. if not, search for the middle space, and split it there (only splits to 2 lines).
        this.ctx.translate(x,y);
        this.ctx.save();
        this.ctx.rotate(rotation);        
        if (this.ctx.measureText(text).width <= maxWidth*0.8){ 
            this.ctx.fillText(text,0,0);
        } else {
            var spl = text.split('-');
            var len = Math.floor(spl.length/2);
            var pos = 0;
            for (var i=0; i<len; i++){
                pos = text.indexOf('-',pos)+1;
            }            
            var text1 = text.substring(0,pos);
            var text2 = text.substring(pos);
            this.ctx.fillText(text1,0,-10);
            this.ctx.fillText(text2,0,+10);
        }
        this.ctx.restore();
        this.ctx.translate(-x,-y);
    }
};