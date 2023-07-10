function downloadImage() {
    var link = document.createElement('a');
        link.download = 'image.png';
        link.href = document.getElementsByTagName('img')[0].src;
        link.click();
        }