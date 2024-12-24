document.addEventListener('DOMContentLoaded', () => {
    // Arka plan temasını değiştiren işlev
        const sunButton = document.getElementById('sun-button');
        const moonButton = document.getElementById('moon-button');
        const body = document.body;

        /*const rightPanel = document.querySelector('.right-panel');
        const leftPanel = document.querySelector('.left-panel');
        const resizeHandleLeft = document.querySelector('.resize-handle-left');
        const resizeHandleRight = document.querySelector('.resize-handle-right');*/

        // Güneş butonuna tıklanınca arka planı aç (gündüz)
        sunButton.addEventListener('click', () => {
            body.classList.add('light-theme');  // Açık tema sınıfını ekle
    body.classList.remove('dark-theme');  // Koyu tema sınıfını kaldır

            body.style.backgroundColor = '#ecf0f1';  // Açık renk
            body.style.color = '#2c3e50';  // Koyu yazı rengi
            leftPanel.style.backgroundColor = '#ecf0f1';  // Sol panel açık renk
            rightPanel.style.backgroundColor = '#ecf0f1';  // Sağ panel açık renk
            leftPanel.style.color = '#2c3e50';  // Sol panel yazı rengi
            rightPanel.style.color = '#2c3e50';  // Sağ panel yazı rengi
            //leftPanelTitle.style.color = '#2c3e50';  // Başlık koyu renk
            //leftPanelText.style.color = '#2c3e50';  // Çıktı içeriği koyu renk
            sunButton.classList.add('active');
            moonButton.classList.remove('active');
        });

        // Ay butonuna tıklanınca arka planı kapat (gece)
        moonButton.addEventListener('click', () => {
            body.classList.add('dark-theme');  // Koyu tema sınıfını ekle
    body.classList.remove('light-theme');  // Açık tema sınıfını kaldır

            body.style.backgroundColor = '#1e2a34';  // Koyu mavi
            body.style.color = '#f4f6f8';  // Açık yazı rengi
            leftPanel.style.backgroundColor = '#2c3e50';  // Sol panel koyu renk
            rightPanel.style.backgroundColor = '#2c3e50';  // Sağ panel koyu renk
            leftPanel.style.color = '#f4f6f8';  // Sol panel yazı rengi
            rightPanel.style.color = '#f4f6f8';  // Sağ panel yazı rengi
            moonButton.classList.add('active');
            sunButton.classList.remove('active');
        });
});

