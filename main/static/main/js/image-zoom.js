document.addEventListener('DOMContentLoaded', function() {
    // Создаем модальное окно для увеличенного изображения
    const zoomModal = document.createElement('div');
    zoomModal.className = 'zoom-modal';
    zoomModal.innerHTML = `
        <div class="zoom-modal-overlay"></div>
        <div class="zoom-modal-content">
            <button class="zoom-modal-close">&times;</button>
            <img class="zoom-modal-image" src="" alt="Увеличенное изображение">
        </div>
    `;
    document.body.appendChild(zoomModal);

    const modalOverlay = zoomModal.querySelector('.zoom-modal-overlay');
    const modalContent = zoomModal.querySelector('.zoom-modal-content');
    const modalImage = zoomModal.querySelector('.zoom-modal-image');
    const closeButton = zoomModal.querySelector('.zoom-modal-close');

    // Функция открытия модального окна
    function openZoomModal(imageSrc, altText) {
        modalImage.src = imageSrc;
        modalImage.alt = altText || 'Увеличенное изображение';
        zoomModal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    // Функция закрытия модального окна
    function closeZoomModal() {
        zoomModal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Функция для добавления обработчиков к большим изображениям
    function addClickHandlersToLargeImages() {
        const sliderForImages = document.querySelectorAll('.slider-for .slider-image');
        sliderForImages.forEach(img => {
            // Убираем старый обработчик, если был
            img.removeEventListener('click', img.clickHandler);
            
            // Создаем новый обработчик
            img.clickHandler = function(e) {
                e.stopPropagation();
                openZoomModal(this.src, this.alt);
            };
            
            // Добавляем новый обработчик
            img.addEventListener('click', img.clickHandler);
            
            // Добавляем указатель курсора
            img.style.cursor = 'pointer';
        });
    }

    // Добавляем обработчики при загрузке
    addClickHandlersToLargeImages();

    // Наблюдаем за изменениями в DOM (на случай, если слайдер обновляется динамически)
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList' || mutation.type === 'subtree') {
                // Проверяем, были ли добавлены новые изображения
                const addedNodes = Array.from(mutation.addedNodes);
                const hasImages = addedNodes.some(node => 
                    node.nodeType === 1 && (node.classList?.contains('slider-image') || node.querySelector?.('.slider-image'))
                );
                
                if (hasImages) {
                    addClickHandlersToLargeImages();
                }
            }
        });
    });

    // Начинаем наблюдение за изменениями в слайдере
    const sliderFor = document.querySelector('.slider-for');
    if (sliderFor) {
        observer.observe(sliderFor, { 
            childList: true, 
            subtree: true 
        });
    }

    // Закрытие по клику на overlay
    modalOverlay.addEventListener('click', closeZoomModal);

    // Закрытие по клику на кнопку закрытия
    closeButton.addEventListener('click', closeZoomModal);

    // Закрытие по клавише Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && zoomModal.classList.contains('active')) {
            closeZoomModal();
        }
    });

    // Предотвращаем закрытие при клике на само изображение
    modalImage.addEventListener('click', function(e) {
        e.stopPropagation();
    });
});