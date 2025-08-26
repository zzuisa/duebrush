jQuery(function($){

var BRUSHED = window.BRUSHED || {};
var API_BASE = window.API_BASE || 'https://roguelife.de';

/* ==================================================
   Mobile Navigation
================================================== */
var mobileMenuClone = $('#menu').clone().attr('id', 'navigation-mobile');


BRUSHED.mobileNav = function(){
	var windowWidth = $(window).width();
	
	if( windowWidth <= 979 ) {
		if( $('#mobile-nav').length > 0 ) {
			mobileMenuClone.insertAfter('#menu');
			$('#navigation-mobile #menu-nav').attr('id', 'menu-nav-mobile');
		}
	} else {
		$('#navigation-mobile').css('display', 'none');
		if ($('#mobile-nav').hasClass('open')) {
			$('#mobile-nav').removeClass('open');	
		}
	}
}

BRUSHED.listenerMenu = function(){
	$('#mobile-nav').on('click', function(e){
		$(this).toggleClass('open');
		if ($('#mobile-nav').hasClass('open')) {
			$('#navigation-mobile').slideDown(500, 'easeOutExpo');
		} else {
			$('#navigation-mobile').slideUp(500, 'easeOutExpo');
		}
		e.preventDefault();
	});
	
	$('#menu-nav-mobile a').on('click', function(){
		$('#mobile-nav').removeClass('open');
		$('#navigation-mobile').slideUp(350, 'easeOutExpo');
	});
}

BRUSHED.mobileNav = function(){
	var windowWidth = $(window).width();
	
	if( windowWidth <= 979 ) {
		if( $('#mobile-nav').length > 0 ) {
			mobileMenuClone.insertAfter('#menu');
			$('#navigation-mobile #menu-nav').attr('id', 'menu-nav-mobile');
		}
	} else {
		$('#navigation-mobile').css('display', 'none');
		if ($('#mobile-nav').hasClass('open')) {
			$('#mobile-nav').removeClass('open');	
		}
	}
}

    // Update active class based on scroll position
    function updateActiveLink() {
        var scrollPosition = $(document).scrollTop();
        
        $('#menu-nav li').each(function() {
            var target = $($(this).find('a').attr('href'));
            
            if (target.length > 0 && target.offset().top <= scrollPosition + 100) {
                $('#menu-nav li').removeClass('current');
                $(this).addClass('current');
            }
        });
    }

    // Run the update when the user scrolls
    $(window).on('scroll', function() {
        // updateActiveLink();
    });

    // Smooth scroll to anchor links and update active class
    $('#menu-nav a').on('click', function(e){
        var target = $($(this).attr('href'));

        if (target.length > 0) {
            $('html, body').animate({
                scrollTop: target.offset().top
            }, 200, 'easeOutExpo');
            e.preventDefault();
        }
    });

    // Initialize active link on page load (for deep links or reloading)
    // updateActiveLink();

/* ==================================================
   Slider Options
================================================== */

BRUSHED.slider = function(){
	function toAbs(url){
		if(!url) return '';
		if(/^https?:\/\//i.test(url)) return url;
		if(url.indexOf('/uploads/') === 0) return API_BASE + url;
		return url; // 允许站点相对路径，如 _include/... 或 /_include/...
	}
	function initSlider(slides){
		$.supersized({
			slideshow:1,
			autoplay:1,
			start_slide:1,
			stop_loop:0,
			random:0,
			slide_interval:12000,
			transition:1,
			transition_speed:300,
			new_window:1,
			pause_hover:0,
			keyboard_nav:1,
			performance:1,
			image_protect:1,
			min_width:0,
			min_height:0,
			vertical_center:1,
			horizontal_center:1,
			fit_always:0,
			fit_portrait:1,
			fit_landscape:0,
			slide_links:'blank',
			thumb_links:0,
			thumbnail_navigation:0,
			slides: slides,
			progress_bar:0,
			mouse_scrub:0
		});
	}
	$.getJSON(API_BASE + '/api/slider').done(function(list){
		if(list && list.length){
			var slides = list.map(function(s){
				var img = toAbs(s.image||'');
				var title = '<div class="slide-content">'+ (s.title||'Düsselbrush') +'</div>';
				return { image: img, title: title, thumb: '', url: '' };
			});
			initSlider(slides);
		}else{
			initSlider([
				{image : '_include/img/slider-images/image01.jpg', title : '<div class="slide-content">Düsselbrush</div>', thumb : '', url : ''},
				{image : '_include/img/slider-images/image02.jpg', title : '<div class="slide-content">Düsselbrush</div>', thumb : '', url : ''}
			]);
		}
	}).fail(function(){
		initSlider([
			{image : '_include/img/slider-images/image01.jpg', title : '<div class="slide-content">Düsselbrush</div>', thumb : '', url : ''},
			{image : '_include/img/slider-images/image02.jpg', title : '<div class="slide-content">Düsselbrush</div>', thumb : '', url : ''}
		]);
	});
}


/* ==================================================
   Navigation Fix
================================================== */

BRUSHED.nav = function(){
	$('.sticky-nav').waypoint('sticky');
}


/* ==================================================
   Filter Works
================================================== */
BRUSHED.filter = function () {
    const $container = $('#thumbs');
    const $optionSets = $('#options .option-set');
    const $optionLinks = $optionSets.find('a');

    // 确保元素存在
    if ($container.length === 0) return;

    // 首屏占位与隐藏，待图片加载完再展示
    $container.css({ minHeight: '400px', visibility: 'hidden' });

    function toAbs(url){
        if(!url) return '';
        if(/^https?:\/\//i.test(url)) return url;
        if(url.indexOf('/uploads/') === 0) return API_BASE + url;
        return url;
    }

    // 拉取画作数据并渲染缩略图
    function renderPaintings(paintings){
        $container.empty();
        var imgTotal = 0, imgDone = 0;

        function markDone(){
            imgDone++;
            if(imgDone >= imgTotal){
                // 初始化或刷新 Isotope
                if(!$container.data('isotope-initialized')){
                    $container.isotope({
                        animationEngine: 'best-available',
                        itemSelector: '.item-thumbs',
                        layoutMode: 'fitRows'
                    });
                    $container.data('isotope-initialized', true);
                } else {
                    $container.isotope('reloadItems');
                }
                $container.isotope({ filter: '*' });
                $container.css({ minHeight: '', visibility: 'visible' });
                $container.isotope('layout');
            }
        }

        paintings.forEach(function(p){
            var classes = 'item-thumbs span3 ' + (p.category || 'design');
            var fullRaw = p.full_image || p.image_full || (p.image && p.image.full) || '';
            var thumbRaw = p.thumb_image || p.image_thumb || (p.image && p.image.thumb) || '';
            var full = toAbs(fullRaw) || '_include/img/work/full/image-01-full.jpg';
            var thumb = toAbs(thumbRaw) || '_include/img/work/thumbs/image-01.jpg';
            var title = p.title || 'Artwork';
            var alt = p.description || '';
            var li = [
                '<li class="'+classes+'">',
                '<a class="hover-wrap fancybox" data-fancybox-group="gallery" title="'+ title.replace(/"/g,'&quot;') +'" href="'+ full +'">',
                '<span class="overlay-img"></span>',
                '<span class="overlay-img-thumb font-icon-plus"></span>',
                '</a>',
                '<img src="'+ thumb +'" alt="'+ alt.replace(/"/g,'&quot;') +'">',
                '</li>'
            ].join('');
            $container.append(li);
            imgTotal++;
        });

        // 若没有图片，直接显示容器
        if(imgTotal === 0){
            if(!$container.data('isotope-initialized')){
                $container.isotope({ animationEngine: 'best-available', itemSelector: '.item-thumbs', layoutMode: 'fitRows' });
                $container.data('isotope-initialized', true);
            }
            $container.css({ minHeight: '', visibility: 'visible' });
        } else {
            // 监听新加图片加载完成
            $container.find('img').each(function(){
                if(this.complete){
                    markDone();
                } else {
                    $(this).one('load error', markDone);
                }
            });
        }

        // 重新绑定 fancybox
        BRUSHED.fancyBox();
    }

    $.getJSON(API_BASE + '/api/paintings')
        .done(function(data){
            renderPaintings(data || []);
        })
        .fail(function(){
            // 回退：不破坏现有静态内容
            $container.css({ minHeight: '', visibility: 'visible' });
            $container.isotope({
                animationEngine: 'best-available',
                itemSelector: '.item-thumbs',
                layoutMode: 'fitRows'
            });
        });

    // 过滤器点击事件
    $optionLinks.on('click', function (e) {
        e.preventDefault();

        const $this = $(this);

        // 如果选项已经被选中，则跳过
        if ($this.hasClass('selected')) {
            return;
        }

        // 更新选中的过滤项
        const $optionSet = $this.closest('.option-set');
        $optionSet.find('.selected').removeClass('selected');
        $this.addClass('selected');

        // 动态生成 options 对象
        const options = {};
        const key = $optionSet.data('option-key');  // 使用 data- 属性直接获取
        let value = $this.data('option-value');    // 使用 data- 属性直接获取

        // 解析 'false' 为布尔值 false
        value = value === 'false' ? false : value;
        options[key] = value;

        // 应用筛选到 #thumbs 容器
        $container.isotope(options);
    });
};


/* ==================================================
   FancyBox
================================================== */

BRUSHED.fancyBox = function(){
	if($('.fancybox').length > 0 || $('.fancybox-media').length > 0 || $('.fancybox-various').length > 0){
		
		$(".fancybox").fancybox({				
				padding : 0,
				beforeShow: function () {
					this.title = $(this.element).attr('title');
					this.title = '<h4>' + this.title + '</h4>' + '<p>' + $(this.element).parent().find('img').attr('alt') + '</p>';
				},
				helpers : {
					title : { type: 'inside' },
				}
			});
			
		$('.fancybox-media').fancybox({
			openEffect  : 'none',
			closeEffect : 'none',
			helpers : {
				media : {}
			}
		});
	}
}


/* ==================================================
   Contact Form
================================================== */

BRUSHED.contactForm = function(){
    var $form = $('#contact-form');
    var $submitBtn = $('#contact-submit');
    var $response = $('#response');
    
    // 清除错误消息
    function clearErrors() {
        $('.error-message').text('');
        $('.error-message').hide();
    }
    
    // 显示错误消息
    function showError(fieldId, message) {
        $('#' + fieldId + '-error').text(message).show();
    }
    
    // 显示响应消息
    function showResponse(message, type) {
        $response.removeClass('success error').addClass(type).text(message).show();
        if (type === 'success') {
            // 成功时3秒后隐藏消息
            setTimeout(function() {
                $response.fadeOut();
            }, 3000);
        }
    }
    
    // 表单验证
    function validateForm() {
        clearErrors();
        var isValid = true;
        
        var name = $('#contact_name').val().trim();
        var email = $('#contact_email').val().trim();
        var message = $('#contact_message').val().trim();
        
        // 验证姓名
        if (!name) {
            showError('name', 'Please enter your name');
            isValid = false;
        }
        
        // 验证邮箱
        if (!email) {
            showError('email', 'Please enter your email address');
            isValid = false;
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            showError('email', 'Please enter a valid email address');
            isValid = false;
        }
        
        // 验证消息
        if (!message) {
            showError('message', 'Please enter your message');
            isValid = false;
        } else if (message.length < 10) {
            showError('message', 'Message must be at least 10 characters long');
            isValid = false;
        }
        
        return isValid;
    }
    
    // 设置加载状态
    function setLoading(loading) {
        if (loading) {
            $submitBtn.prop('disabled', true);
            $submitBtn.find('.submit-text').hide();
            $submitBtn.find('.loading-text').show();
        } else {
            $submitBtn.prop('disabled', false);
            $submitBtn.find('.submit-text').show();
            $submitBtn.find('.loading-text').hide();
        }
    }
    
    // 表单提交处理
    $form.on('submit', function(e) {
        e.preventDefault();
        
        if (!validateForm()) {
            return false;
        }
        
        setLoading(true);
        clearErrors();
        
        var formData = {
            name: $('#contact_name').val().trim(),
            email: $('#contact_email').val().trim(),
            message: $('#contact_message').val().trim()
        };
        
        $.ajax({
            type: "POST",
            url: API_BASE + "/api/contact",
            data: JSON.stringify(formData),
            contentType: "application/json",
            dataType: 'json',
            success: function(response) {
                setLoading(false);
                if (response.success) {
                    showResponse(response.message || 'Message sent successfully! We will get back to you soon.', 'success');
                    // 清空表单
                    $form[0].reset();
                } else {
                    showResponse(response.message || 'Failed to send message. Please try again later.', 'error');
                }
            },
            error: function(xhr) {
                setLoading(false);
                var errorMessage = 'Failed to send message. Please try again later.';
                
                if (xhr.responseJSON && xhr.responseJSON.message) {
                    errorMessage = xhr.responseJSON.message;
                } else if (xhr.status === 0) {
                    errorMessage = 'Network connection failed. Please check your internet connection.';
                } else if (xhr.status === 500) {
                    errorMessage = 'Server error. Please try again later.';
                }
                
                showResponse(errorMessage, 'error');
            }
        });
        
        return false;
    });
    
    // 实时验证
    $('#contact_name, #contact_email, #contact_message').on('blur', function() {
        var fieldId = $(this).attr('id');
        var value = $(this).val().trim();
        
        // 清除当前字段的错误
        $('#' + fieldId + '-error').text('').hide();
        
        // 验证当前字段
        if (fieldId === 'contact_name' && !value) {
            showError('name', 'Please enter your name');
        } else if (fieldId === 'contact_email') {
            if (!value) {
                showError('email', 'Please enter your email address');
            } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                showError('email', 'Please enter a valid email address');
            }
        } else if (fieldId === 'contact_message') {
            if (!value) {
                showError('message', 'Please enter your message');
            } else if (value.length < 10) {
                showError('message', 'Message must be at least 10 characters long');
            }
        }
    });
    
    // 输入时清除错误
    $('#contact_name, #contact_email, #contact_message').on('input', function() {
        var fieldId = $(this).attr('id');
        $('#' + fieldId + '-error').text('').hide();
    });
}


/* ==================================================
   Twitter Feed
================================================== */

BRUSHED.tweetFeed = function(){
	var valueTop = -64;
	
    $("#ticker").tweet({
          username: "Bluxart",
          page: 1,
          avatar_size: 0,
          count: 10,
		  template: "{text}{time}",
		  filter: function(t){ return ! /^@\w+/.test(t.tweet_raw_text); },
          loading_text: "loading ..."
	}).bind("loaded", function() {
	  var ul = $(this).find(".tweet_list");
	  var ticker = function() {
		setTimeout(function() {
			ul.find('li:first').animate( {marginTop: valueTop + 'px'}, 500, 'linear', function() {
				$(this).detach().appendTo(ul). removeAttr('style');
			});	
		  ticker();
		}, 5000);
	  };
	  ticker();
	});
	
}


/* ==================================================
   Menu Highlight
================================================== */

BRUSHED.menu = function(){
	$('#menu-nav, #menu-nav-mobile').onePageNav({
		currentClass: 'current',
    	changeHash: false,
    	scrollSpeed: 750,
    	scrollOffset: 30,
    	scrollThreshold: 0.5,
		easing: 'easeOutExpo',
		filter: ':not(.external)'
	});
}

/* ==================================================
   Next Section
================================================== */

BRUSHED.goSection = function(){
	$('#nextsection').on('click', function(){
		$target = $($(this).attr('href')).offset().top-30;
		
		$('body, html').animate({scrollTop : $target}, 750, 'easeOutExpo');
		return false;
	});
}

/* ==================================================
   GoUp
================================================== */

BRUSHED.goUp = function(){
	$('#goUp').on('click', function(){
		$target = $($(this).attr('href')).offset().top-30;
		
		$('body, html').animate({scrollTop : $target}, 750, 'easeOutExpo');
		return false;
	});
}


/* ==================================================
	Scroll to Top
================================================== */

BRUSHED.scrollToTop = function(){
	var windowWidth = $(window).width(),
		didScroll = false;

	var $arrow = $('#back-to-top');

	$arrow.click(function(e) {
		$('body,html').animate({ scrollTop: "0" }, 750, 'easeOutExpo' );
		e.preventDefault();
	})

	$(window).scroll(function() {
		didScroll = true;
	});

	setInterval(function() {
		if( didScroll ) {
			didScroll = false;

			if( $(window).scrollTop() > 1000 ) {
				$arrow.css('display', 'block');
			} else {
				$arrow.css('display', 'none');
			}
		}
	}, 250);
}

/* ==================================================
   Thumbs / Social Effects
================================================== */

BRUSHED.utils = function(){
	
	$('.item-thumbs').bind('touchstart', function(){
		$(".active").removeClass("active");
      	$(this).addClass('active');
    });
	
	$('.image-wrap').bind('touchstart', function(){
		$(".active").removeClass("active");
      	$(this).addClass('active');
    });
	
	$('#social ul li').bind('touchstart', function(){
		$(".active").removeClass("active");
      	$(this).addClass('active');
    });
	
}

/* ==================================================
   Accordion
================================================== */

BRUSHED.accordion = function(){
	var accordion_trigger = $('.accordion-heading.accordionize');
	
	accordion_trigger.delegate('.accordion-toggle','click', function(event){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
		   	$(this).addClass('inactive');
		}
		else{
		  	accordion_trigger.find('.active').addClass('inactive');          
		  	accordion_trigger.find('.active').removeClass('active');   
		  	$(this).removeClass('inactive');
		  	$(this).addClass('active');
	 	}
		event.preventDefault();
	});
}

/* ==================================================
   Toggle
================================================== */

BRUSHED.toggle = function(){
	var accordion_trigger_toggle = $('.accordion-heading.togglize');
	
	accordion_trigger_toggle.delegate('.accordion-toggle','click', function(event){
		if($(this).hasClass('active')){
			$(this).removeClass('active');
		   	$(this).addClass('inactive');
		}
		else{
		  	$(this).removeClass('inactive');
		  	$(this).addClass('active');
	 	}
		event.preventDefault();
	});
}

/* ==================================================
   Tooltip
================================================== */

BRUSHED.toolTip = function(){ 
    $('a[data-toggle=tooltip]').tooltip();
}


/* ==================================================
	Init
================================================== */

BRUSHED.slider();

$(document).ready(function(){

	// Preload the page with jPreLoader
	$('body').jpreLoader({
		splashID: "#jSplash",
		showSplash: true,
		showPercentage: true,
		autoClose: true,
		splashFunction: function() {
			$('#circle').delay(250).animate({'opacity' : 1}, 500, 'linear');
		}
	});
	
	BRUSHED.nav();
	BRUSHED.mobileNav();
	BRUSHED.listenerMenu();
	BRUSHED.menu();
	BRUSHED.goSection();
	BRUSHED.goUp();
	BRUSHED.filter();
	BRUSHED.fancyBox();
	BRUSHED.contactForm();
	BRUSHED.tweetFeed();
	BRUSHED.scrollToTop();
	BRUSHED.utils();
	BRUSHED.accordion();
	BRUSHED.toggle();
	BRUSHED.toolTip();
});

$(window).resize(function(){
	BRUSHED.mobileNav();
});

});
