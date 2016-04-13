var p2pApp = angular.module('p2pApp', ['p2pFilters', 'ngMaterial']);

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

  $scope.filterMonth = function(minMonth, maxMonth, monthFilter) {
    minMonth = minMonth == undefined ? 0 : minMonth;
    maxMonth = maxMonth == undefined ? 1000 : maxMonth;
    $scope.monthFilter = monthFilter;
    $scope.loans = filterBy(rawLoans, function(loan, index, array) {
      return loan.fields.duration / 30 >= minMonth
          && loan.fields.duration / 30 <= maxMonth;
    });
  };

})
.directive('p2pContainer', function() {
  return {
    templateUrl: '/static/p2p/ng-tmp/p2p.html'
  };
});
