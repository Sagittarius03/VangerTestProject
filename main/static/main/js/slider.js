$(document).ready(function(){
            // Инициализация главного слайдера
            $('.slider-for').slick({
                autoplay: true,
                slidesToShow: 1,
                slidesToScroll: 1,
                arrows: false,
                fade: false,
                asNavFor: '.slider-nav'
            });
            
            // Инициализация навигационного слайдера с адаптивными настройками
            $('.slider-nav').slick({
                slidesToShow: 4,
                slidesToScroll: 1,
                asNavFor: '.slider-for',
                dots: false,
                centerMode: true,
                focusOnSelect: true,
                arrows: true,
                
            });
        });