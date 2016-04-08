var p2pApp = angular.module('p2pApp', []);

p2pApp.controller('P2pController', function ($scope, $http) {

  $http.get('/p/loans-json/').success(function(data) {
    $scope.loans = data;
  });

  $http.get('/p/platforms-json/').success(function(data) {
    platforms = {};
    for (i in data) {
      p = data[i];
      platforms[p.pk] = p.fields;
    }
    $scope.platforms = platforms;
  });

})
.directive('p2pContainer', function() {
  return {
    templateUrl: '/static/p2p/ng-tmp/p2p.html'
  };
});
