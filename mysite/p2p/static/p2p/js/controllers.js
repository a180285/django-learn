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

  $scope.selected = [];

  $scope.toggle = function (item, list) {
    var idx = list.indexOf(item);
    if (idx > -1) {
      list.splice(idx, 1);
    }
    else {
      list.push(item);
    }
  };

  $scope.exists = function (item, list) {
    return list.indexOf(item) > -1;
  };

  $scope.isIndeterminate = function() {
    return ($scope.selected.length !== 0 &&
        $scope.selected.length !== $scope.platformsArray.length);
  };

  $scope.isAllChecked = function() {
    return $scope.selected.length === $scope.platformsArray.length;
  };

  $scope.toggleAll = function() {
    if ($scope.selected.length === $scope.platformsArray.length) {
      $scope.selected = [];
    } else if ($scope.selected.length === 0 || $scope.selected.length > 0) {
      $scope.selected = $scope.platformsArray.slice(0);
    }
  };

})
.directive('p2pContainer', function() {
  return {
    templateUrl: '/static/p2p/ng-tmp/p2p.html'
  };
});
