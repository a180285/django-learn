var p2pApp = angular.module('p2pApp', ['p2pFilters', 'ngMaterial']);

p2pApp.controller('P2pController', function ($scope, $http, $filter) {
  var orderBy = $filter('orderBy');
  var filterBy = $filter('filter');

  var rawLoans = [];
  var platformIds = [];

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
      platformIds.push(p.pk);
    }
    $scope.platforms = platforms;
    $scope.platformsArray = data;
  });

  $scope.reverse = true;
  $scope.order = function(predicate) {
    $scope.reverse = ($scope.predicate === predicate) ? !$scope.reverse : false;
    $scope.predicate = predicate;
  };

  $scope.filterByPlatform = function(loan, loans, index) {
    return $scope.selected.length == 0 || $scope.selected.indexOf(loan.fields.platform) > -1;
  }

  $scope.filterMonth = function(minMonth, maxMonth, monthFilter) {
    minMonth = minMonth == undefined ? 0 : minMonth;
    maxMonth = maxMonth == undefined ? 1000 : maxMonth;
    $scope.monthFilter = monthFilter;
    $scope.loans = filterBy(rawLoans, function(loan, index, array) {
      return loan.fields.duration / 30 >= minMonth
          && loan.fields.duration / 30 <= maxMonth;
    });
  };

  $scope.selected = localStorage.getItem('platform_selected');
  if ($scope.selected) {
    $scope.selected = $scope.selected.split(',').map(Number);
  } else {
    $scope.selected = [];
  }

  $scope.toggle = function (item, list) {
    var idx = list.indexOf(item);
    if (idx > -1) {
      list.splice(idx, 1);
    } else {
      list.push(item);
    }

    localStorage.setItem('platform_selected', list)
  };

  $scope.exists = function (item, list) {
    return list.indexOf(item) > -1;
  };

  $scope.isIndeterminate = function() {
    return ($scope.selected.length != 0 &&
        $scope.selected.length != platformIds.length);
  };

  $scope.isAllChecked = function() {
    return $scope.selected.length === platformIds.length;
  };

  $scope.toggleAll = function() {
    if ($scope.selected.length == platformIds.length) {
      $scope.selected = [];
    } else {
      $scope.selected = platformIds.slice(0);
    }
    localStorage.setItem('platform_selected', $scope.selected)
  };

})
.directive('p2pContainer', function() {
  return {
    templateUrl: '/static/p2p/ng-tmp/p2p.html'
  };
});
