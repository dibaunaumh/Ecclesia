Node = function(config) {
	this.config = {
		dimensions	: {},
		id			: -1,
		url			: '',
		name		: '',
		label		: ''
	};
	this.data = {};
	this.ready = false;
	if(config != null) {
		$.extend(true, this.config, config);
	}
};
Node.prototype = {
	toString	: function() {
		return this.config.name;
	},
	prepareData	: function() {
		var this_ = this;
		$.each(this.config.dimensions, function(key, val) {
			// creating a mapped object in format of: { dimension_id:value, ... }
			$.extend(this_.data, eval('{'+key+'_'+this_.config.id+':'+val+'}');
		});
	},
	serialize	: function() {
		this.prepareData();
		return $.param(this.data) + '&pk=' + this.config.id;
	},
	loadImage	: function() {
		// setting the background image and making sure the image is loaded
		if(this.config.bg_image && this.config.bg_src) {
			this.config.bg_image.src = this.config.bg_src;
			var this_ = this;
			$(this.config.bg_image).load(function() {
				this_.ready = true;
			});
		}
	}
};

Group = function(Node) {
	this.config = {
		alias	: 'group',
		model	: 'GroupProfile',
		bg_src	: '/static/img/cork_board.jpg',
		bg_image: new Image()
	};
	this.loadImage();
	// inheriting Node class
	this = $.extend(true, {}, Node, this);
};
Group.prototype = {
	serialize	: function() {
		this.prepareData();
		return $.param(this.data) + '&model=' + this.config.model + '&pk=' + this.config.id;
	}
};

Discussion = function(Node) {
	this.config = {
		alias	: 'disc',
		model	: 'Discussion',
		bg_src	: '/static/img/whiteboard.jpg',
		bg_image: new Image()
	};
	this.loadImage();
	// inheriting Node class
	this = $.extend(true, {}, Node, this);
};
Discussion.prototype = {
	serialize	: function() {
		this.prepareData();
		return $.param(this.data) + '&model=' + this.config.model + '&pk=' + this.config.id;
	}
};

VUController = function(options) {
	this.options = {
		width		: 900,
		height		: 600,
		container_id: 'canvasContainer',
		canvas_id	: 'groupsvu',
		data_url	: '/groups/get_view_elements/',
		update_url	: '/common/update_coords/'
	};
	if(options != null) {
		$.extend(this.options, options);
	}
	//this.options.update_url = this.options.update_url + this.options.type;
	
	this.data = {};
	this.elems = {};
	this.drag = {};
	this.ctx = null;
	var this_ = this;
	$(this.img).load(function(){
		this_.init();
	});
};
VUController.prototype = {
	getData			: function() {
		var this_ = this;
		// expecting format: [ { element_alias : { element_config_object }, ... ]
		$.getJSON(this.options.data_url + this.options.model, function(data){
			this_.data = data;
			//alert(this_.data);
			return true;
		});
	},
	createNodes		: function() {
		var this_ = this;
		$.each(this.data, function(i, item) {
			$.each(item, function(key, val) {
				var node = new Node(val);
				switch(key) {
					case 'group':
						node = new Group(node);
						break;
					case 'discussion':
						node = new Discussion(node);
						break;
					case 'story':
						node = new Story(node);
						break;
					case 'relation':
						node = new Relation(node);
						break;
					case 'opinion':
						node = new Opinion(node);
						break;
				}
				this_.elems[node.config.id] = node;
			});
		});
	},
	initCanvas		: function() {
		var o = this.options;
		$('#'+o.container_id).empty();
		$('#'+o.container_id).append('<canvas id="'+o.canvas_id+'" width="'+o.width+'" height="'+o.height+'"></canvas>');
		this.ctx = document.getElementById(o.canvas_id).getContext('2d');
		return (this.ctx != null);
	},
	setDraggable	: function(el) {
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
					this_.elems[id].config.dimensions.x = position.left;
					this_.elems[id].config.dimensions.y = position.top;
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
	addElement		: function(el) {
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
	init			: function() {
		// get the json containing all the elements' configs
		if(this.getData()) {
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
		} else {
			alert('Failed to recive data.');
		}
	},
	position		: function(id) {
		var config = this.elems[id].config;
		var id_selector = '#'+config.alias+'_'+id;
		$(id_selector).css('left', config.dimensions.x+'px');
		$(id_selector).css('top', config.dimensions.y+'px');
	},
	setDrag			: function(dom_id) {
		var temp = dom_id.split('_');
		this.drag = this.elems[temp[1]];
	},
	_draw			: function(id) {
		if(this.elems[id].ready) {
			var config = this.elems[id].config;
			try {
				this.ctx.drawImage(config.bg_image, config.dimesions.x, config.dimesions.y, config.dimesions.w, config.dimesions.h);
			} catch(e) {}
		} else {
			//this._draw(id);
		}
	},
	draw			: function(isGrip) {
		var this_ = this;
		this.ctx.clearRect(0, 0, this.options.width, this.options.height);
		$.each(this.elems, function(id, el) {
			if(isGrip) {
				if(id != this_.drag.config.id) {
					this_._draw(id);
				}
			} else {
				this_._draw(id);
			}
		});
	},
	grip			: function() {
		$('#'+this.drag.config.alias+'_'+this.drag.config.id).addClass('dragon');
		this.draw(true);
	},
	drop			: function() {
		$('#'+this.drag.config.alias+'_'+this.drag.config.id).removeClass('dragon');
		this.draw();
		this.updateCoords();
	},
	updateCoords	: function() {
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