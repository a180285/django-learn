var p2pApp = angular.module('p2pApp', []);

p2pApp.controller('P2pController', function ($scope, $http, $filter) {
  var orderBy = $filter('orderBy');

  $http.get('/p/loans-json/').success(function(data) {
    $scope.loans = data;
  });

  $http.get('/p/platforms-json/').success(function(data) {
    platforms = {};
    platformsArray = [];
    for (i in data) {
      p = data[i];
      platforms[p.pk] = p.fields;
    }
    $scope.platforms = platforms;
    $scope.platformsArray = data;
  });

  $scope.reverse = true;
  $scope.order = function(predicate) {
    $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
    $scope.predicate = predicate;
    $scope.loans = orderBy($scope.loans, predicate, $scope.reverse);
  };

})
.directive('p2pContainer', function() {
  return {
    templateUrl: '/static/p2p/ng-tmp/p2p.html'
  };
});
