$(document).ready(function() {
		
	$(document).ready(function(){ 

	

		$('#js-submit').on('click', function(e){
			//e.preventDefault();	
			//$(this).submit();
			//alert('x')
			return true;
		});


		$('.js-ajax').on('focusout', function(e){
		
			var input = $(this);
			var value = input.val();
			var title 	= $("input[name=title]").val();
			var blog_id = $("input[name=blog_id]").val();
			var date = $("input[name=date]").val();
			var description = $("textarea[name=description]").val();
		
			JMM.router.make_request('/blog/update', { 
					 'title' 	: title, 
					 'date' 	: date, 
					 'description' 	: description, 
					 'blog_id'	: blog_id,
					}, null, null, {
				 		'request_type' : 'GET',
			            'success' : function(data) {
							location.href = data.next_url;
					}
			});			
		})	
	
	
		$('.js-delete').on("click", function(){
		
			console.log('xxxxx')
		
			var blog_id = $(this).data("post_id");
			var answer = confirm("Are you sure you want to delete this post?");
			if (!answer){
				return false
			}
			JMM.router.make_request('/blog/delete', { 
					 'blog_id'	: blog_id,
					}, null, null, {
				 		'request_type' : 'GET',
			            'success' : function(data) {
							location.href = '/blog/new';
					}
			});	
		
			return false;
		});
	
	});






	JMM.ElementsRouter = Backbone.Router.extend({
	
		routes : {		
		},
	
		init: function(options) {
				
			this.ajax = {};
			this.ajax['rapid']		 = $.manageAjax.create('rapid', {queue: false});
			this.ajax['queue']		 = $.manageAjax.create('queue', {queue: true}); 
			this.ajax['queue_clear'] = $.manageAjax.create('queue_clear', {queue: 'clear'}); 
			$.ajaxSettings.traditional = true;
		},
		
		make_request: function(url, data, callback, error_callback, options) {
			var self = this;
			var options = $.extend({
				'ajax_group': 'rapid',
				'traditional': true,
				'domSuccessTrigger': true,
				'preventDoubleRequests': false
			}, options);
			var request_type = options.request_type || 'POST';
			var clear_queue = false;

			this.ajax[options['ajax_group']].add(_.extend({
				url: url,
				data: data,
				type: request_type,
				cache: false,
				cacheResponse: false,
				beforeSend: function() {
					$.isFunction(options['beforeSend']) && options['beforeSend']();
					return true;
				},
				success: function(o) {				
					if (o && o.code < 0 && error_callback) {
						error_callback(o);
					} else if ($.isFunction(callback)) {
						callback(o);
					}
				},
				error: function(e, textStatus, errorThrown) {
					if (errorThrown == 'abort') {
						return;
					}
					JMM.log(['AJAX Uploader Error', e, e.status, textStatus, errorThrown, 
								  !!error_callback, error_callback, $.isFunction(callback)]);
				
					if (error_callback) {
						error_callback(e, textStatus, errorThrown);
					} else if ($.isFunction(callback)) {
						var message = "Please create an account. Not much to do without an account.";
						if (TCB.Globals.is_authenticated) {
						  message = "Sorry, there was an unhandled error.";
						}
						callback({'message': message, status_code: e.status});
					}
				}
			}, options));
	
		},
	
		make_file_upload_request: function(url, button_name, button_id, oncomplete_callback, error_callback, options, params) { 
			var self = this;
			var options = $.extend({}, options);	
			var params = $.extend({
				  'csrf_token'	: $('input[name=csrfmiddlewaretoken]').val(),
			      'csrf_name'	: 'csrfmiddlewaretoken',
			      'csrf_xname'	: 'X-CSRFToken',
			}, params);	
				
			var theUploaderObject = new qq.FileUploader( {
			    action: url,
				onProgress: function(id, fileName, loaded, total) {
					$.isFunction(options['onProgress']) && options['onProgress']();
					return true;
				},
				button_name : button_name,
			    element: $(button_id)[0],
			    multiple: true,
				onSubmit: function(o) {
					$('#uploading_material').modal('show');
				},
			    onComplete: function( o, fileName, responseJSON ) {
					if(responseJSON.success){
						$.isFunction(options['success']) && options['success']();
						return true;
					}
					else if (o && o.code < 0 && error_callback) {
						error_callback(o);
					} else if ($.isFunction(oncomplete_callback)) {
						oncomplete_callback(o, fileName, responseJSON);
					}
				},
				showMessage: function(message){ alert('message : ' + message); },
			
			    onAllComplete: function( uploads ) {},
			    params: params,
			});
		
			return false;
		},

	});

	function statusBar_beforeSend() {
		var loadingBar = $("<div id='loadingbar'></div>");
		$("body").append(loadingBar);
		return loadingBar
			.addClass("waiting")
			.append($("<dt/><dd/>"))
			.width((50 + Math.random() * 30) + "%");
	}

	function statusBar_success() {
		$("#loadingbar").width("101%").delay(10).fadeOut(400, function() {
			$(this).remove();
		});
	}


	$(document).ready(function() {	
		JMM.router = new JMM.ElementsRouter()
		JMM.router.init();
		Backbone.history.start();
	})
 
});

