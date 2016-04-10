angular.module('p2pFilters', [])
.filter('showDuration', function() {
  return function(duration) {
    if (duration >= 30) {
      return duration / 30 + ' 月';
    } else {
      return duration + ' 天';
    }
  };
});
