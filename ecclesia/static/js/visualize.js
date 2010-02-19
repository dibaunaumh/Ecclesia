Node = function(config) {
	this.config = {
		dimensions	: {},
		id			: -1,
		url			: '',
		name		: ''
	};
	if(config !== null) {
		$.extend(true, this.config, config);
	}
};
Node.prototype = {
	toString	: function() {
		return this.config.name;
	},
	serialize	: function() {
		return $.param(this.config.dimensions) + '&pk=' + this.config.id;
	},
	loadImage	: function() {
		// setting the background image and making sure the image is loaded
		if(this.config.bg_image && this.config.bg_src) {
			this.config.bg_image.src = this.config.bg_src;
		}
	}
};

Group = function(node_class, config) {
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
	$.extend(this.config, config);
	this.loadImage();
};
Group.prototype = {
	serialize	: function() {
		return $.param(this.config.dimensions) + '&model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	draw		: function(ctx) {
		var dims = this.config.dimensions;
		if(this.config.bg_image) {
			try {
				ctx.drawImage(this.config.bg_image, dims.x, dims.y, dims.w, dims.h);
			} catch(e){}
			ctx.strokeRect(dims.x, dims.y, dims.w, dims.h);
		}
	}
};

Discussion = function(node_class, config) {
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
	$.extend(this.config, config);
	this.loadImage();
};
Discussion.prototype = {
	serialize	: function() {
		return $.param(this.config.dimensions) + '&model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	draw		: function(ctx) {
		var dims = this.config.dimensions;
		if(this.config.bg_image) {
			try {
				ctx.drawImage(this.config.bg_image, dims.x, dims.y, dims.w, dims.h);
			} catch(e){}
		}
	}
};

Story = function(node_class, config) {
	this.config = {
		alias		: 'story',
		model_name	: 'Story',
		type		: 'goal'
	};
	// inheriting Node class
	var dummy = $.extend(true, node_class, this);
	$.extend(true, this, dummy);
	// reconfig
	$.extend(this.config, config);
};
Story.prototype = {
	serialize	: function() {
		return $.param(this.config.dimensions) + '&model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	roundedRect	: function(ctx,x,y,width,height,radius){
		ctx.save();
		// init the colors
		ctx.fillStyle = "#eee";
		ctx.strokeStyle = "#444";
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
    },
	draw		: function(ctx) {
		var dims = this.config.dimensions;
		this.roundedRect(ctx, dims.x, dims.y, dims.w, dims.h, 5);
	}
};
Relation = new function(node_class, config) {
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
	$.extend(this.config, config);
};
Relation.prototype = {
	serialize	: function() {
		return 'model_name=' + this.config.model_name + '&pk=' + this.config.id;
	},
	toString	: function() {
		return "("+this.from.toString()+","+this.to.toString()+")";
    },
	bezier		: function(ctx,x1,y1,x2,y2,label) {
		ctx.save();
		ctx.beginPath();
		ctx.lineWidth = 4;
		ctx.strokeStyle="rgb(130,130,200)";
		ctx.moveTo(x1,y1);
		ctx.bezierCurveTo(x1 + (x2-x1)/5,y1,x2-(x2-x1)/5,y2,x2,y2);
		ctx.stroke();
		//drawText(label,(x1+x2)/2, (y1+y2)/2, x2-x1,Math.atan2(y2-y1,x2-x1));
		ctx.restore();
    },
	draw		: function(ctx) {
		/*// get the dimensions of the from and to elements
		var from_dims = this.from.cofig.dimensions;
		var to_dims = this.to.cofig.dimensions;
		// calculate the from and to points
		var x1 = from_dims.x + from_dims.w;
		var y1 = from_dims.y + from_dims.h/2;
		var x2 = to_dims.x
		var y2 = to_dims.y + to_dims.h/2;
		// draw it
		this.bezier(ctx, x1, y1, x2, y2);*/
	}
};

VUController = function(options) {
	this.options = {
		width		: 900,
		height		: 600,
		container_id: 'canvasContainer',
		canvas_id	: 'groupsvu',
		data_url	: '/get_groups_view_json/',
		update_url	: '/common/update_presentation/'
	};
	if(options !== null) {
		$.extend(this.options, options);
	}
	
	this.data = {};
	this.elems = {};
	this.drag = {};
	this.ctx = null;
	
	this.getData();
};
VUController.prototype = {
	getData				: function() {
		var this_ = this;
		// expecting format: [ { element_alias : { element_config_object }, ... ]
		$.getJSON(this.options.data_url, function(data){
			this_.data = data;
			// initialize the view controller
			this_.init();
		});
	},
	createNodes			: function() {
		var this_ = this;
		$.each(this.data, function(i, item) {
			$.each(item, function(key, val) {
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
				var id = node.config.id;
				// add the Node instance to the controller's elements
				this_.elems[id] = node;
				// set a load event listener to the element's background image to initialy draw it
				if(node.config.bg_image) {
					$(node.config.bg_image).load(function() {
						node.draw(this_.ctx);
					});
				}
			});
		});
	},
	initCanvas			: function() {
		var o = this.options;
		$('#'+o.container_id).empty();
		$('#'+o.container_id).append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		this.ctx = document.getElementById(o.canvas_id).getContext('2d');
		return (this.ctx !== null);
	},
	setDraggable		: function(el) {
		var this_ = this;
		// set a specific element as draggable
		if(el) {
			var id = el.config.id;
			$('#'+el.config.alias+'_'+id).draggable({
				containment: 'parent',
				start: function(e, ui) {
					this_.setDrag(this.id);
					this_.grip();
				},
				stop : function(e, ui) {
					var position = $(this).position();
					this_.elems[id].config.dimensions.x = parseInt(position.left);
					this_.elems[id].config.dimensions.y = parseInt(position.top);
					this_.drop();
				}
			});
		}
		// set all elements as draggable
		else {
			$.each(this.elems, function(id, el) {
				this_.setDraggable(el);
			});
		}
	},
	addElement			: function(el) {
		// add an element to the DOM
		if(el) {
			var config = el.config;
			$('#'+this.options.container_id).append('<div class="'+config.alias+'" id="'+config.alias+'_'+config.id+'"><a href="'+config.url+'">'+config.name+'</a></div>');
		}
		// add all elements to the DOM
		else {
			var this_ = this;
			$.each(this.elems, function(id, el) {
				this_.addElement(el);
			});
		}
	},
	init				: function() {
		// create the elements
		this.createNodes();
		// initialize the canvas
		if(this.initCanvas()) {
			var this_ = this;
			// iterate over the elements and create the GUI
			$.each(this.elems, function(id, el) {
				// appending a div for each element to the canvas container
				this_.addElement(el);
				// position the element inside the container
				this_.position(id);
				// set it as draggable
				this_.setDraggable(el);
			});
			// we have initialized the canvas so draw the element
			this.draw();
		} else {
			alert('No canvas context.');
		}
	},
	position			: function(id) {
		var config = this.elems[id].config;
		var id_selector = '#'+config.alias+'_'+id;
		$(id_selector).css('left', config.dimensions.x+'px');
		$(id_selector).css('top', config.dimensions.y+'px');
	},
	setDrag				: function(dom_id) {
		var temp = dom_id.split('_');
		this.drag = this.elems[temp[1]];
	},
	draw				: function(isGrip) {
		var this_ = this;
		this.ctx.clearRect(0, 0, this.options.width, this.options.height);
		$.each(this.elems, function(id, el) {
			if(isGrip) {
				if(id != this_.drag.config.id) {
					el.draw(this_.ctx);
				}
			} else {
				el.draw(this_.ctx);
			}
		});
	},
	grip				: function() {
		$('#'+this.drag.config.alias+'_'+this.drag.config.id).addClass('dragon');
		this.draw(true);
	},
	drop				: function() {
		$('#'+this.drag.config.alias+'_'+this.drag.config.id).removeClass('dragon');
		this.draw();
		this.updatePresentation();
	},
	updatePresentation	: function() {
		var this_ = this;
		/*$.each(this.elems, function(id, el){
			this_.data[id] = el.serialize();
		});*/
		this.data = this.drag.serialize();
		
		$.ajax({
			type		: "POST",
			url			: this_.options.update_url,
			data		: this_.data,
			success		: function(msg){
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
DiscussionController = function(VuController, options) {
	this.options = {};
	if(options != null) {
		$.extend(this.options, options);
	}
	// inheriting Node class
	var dummy = $.extend(true, VuController, this);
	$.extend(true, this, dummy);
};
DiscussionController.prototype = {
	createSpeechActContainers	: function() {
		$('#'+this.options.container_id).append('<div id="course_of_action_container" class="stories_container"></div><div id="possible_result_container" class="stories_container"></div><div id="goal_condition_container" class="stories_container"></div><div id="goal_container" class="stories_container"></div>');
		$('#'+this.options.container_id).css('position', 'relative');
		$('.stories_container').height(this.options.height);
		$('.stories_container').width(this.options.width * 0.25);
	},
	initCanvas			: function() {
		var o = this.options;
		$('#'+o.container_id).empty();
		$('#'+o.container_id).append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		this.createSpeechActContainers();
		this.ctx = document.getElementById(o.canvas_id).getContext('2d');
		return (this.ctx !== null);
	},
	addElement			: function(el) {
		// add an element to the DOM
		if(el) {
			var config = el.config;
			$('#'+config.type+'_container').append('<div class="'+config.alias+'" id="'+config.alias+'_'+config.id+'"><a href="'+config.url+'">'+config.name+'</a></div>');
		}
		// add all elements to the DOM
		else {
			var this_ = this;
			$.each(this.elems, function(id, el) {
				this_.addElement(el);
			});
		}
	},
	drawText			: function(text,x,y,maxWidth,rotation) {
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