// Get all videos.
var videos = document.querySelectorAll('video');

// Create a promise to wait all videos to be loaded at the same time.
// When all of the videos are ready, call resolve().
var promise = new Promise(function(resolve) {
  var loaded = 0;

  videos.forEach(function(v) {
    v.addEventListener('loadedmetadata', function() {
      loaded++;

      if (loaded === videos.length) {
        resolve();
      }
    });
  });
});

// Play all videos one by one only when all videos are ready to be played.
promise.then(function() {
  videos.forEach(function(v) {
    v.play();
  });
});