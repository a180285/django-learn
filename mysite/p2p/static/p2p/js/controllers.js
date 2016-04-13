var p2pApp = angular.module('p2pApp', ['p2pFilters']);

p2pApp.controller('P2pController', function ($scope, $http, $filter) {
  var orderBy = $filter('orderBy');
  var filterBy = $filter('filter');

  var rawLoans = [];

  $http.get('/p/loans-json/').success(function(data) {
    rawLoans = data;
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
  };

  $scope.filterMonth = function(minMonth = null, maxMonth = null, monthFilter = null) {
    $scope.monthFilter = monthFilter;
    $scope.loans = filterBy(rawLoans, function(loan, index, array) {
      return (minMonth == undefined || loan.fields.duration / 30 >= minMonth)
          && (maxMonth == undefined || loan.fields.duration / 30 <= maxMonth);
    });
  };

})
.directive('p2pContainer', function() {
  return {
    templateUrl: '/static/p2p/ng-tmp/p2p.html'
  };
});
