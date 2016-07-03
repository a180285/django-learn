var financialApp = angular.module('financialApp', ['ngMaterial']);

financialApp.directive('financialContainer', function() {
  return {
    templateUrl: '/static/financial/ng-tmp/financial.html',
    controller: FinancialController,
    controllerAs: 'FinancialCtrl'
  };
});

var FinancialController = function ($scope, $http) {
  this.scope_ = $scope;
  this.http_ = $http;
  this.accounts_ = [];

  this.newAccount = {name: ''};

  this.init();
}

FinancialController.prototype.init = function() {
  var ctrl = this;
  this.http_.get('/f/accounts-json/').success(function(data) {
    ctrl.accounts_ = data;
  });
}

FinancialController.prototype.getAccounts = function() {
  return this.accounts_;
}

FinancialController.prototype.changeEditingStatus = function(account) {
  if (account.isEditing) {

    var data = {
        csrfmiddlewaretoken: this.scope_.csrfToken};
    for (var key in account.fields) {
      data[key] = account.fields[key];
    }

    data = decodeURIComponent($.param(data));

    this.http_({
      method: 'POST',
      url: '/f/update-account-' + account.pk + '/',
      data: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(null, function() {
      alert('Failed to update account')
      account.isEditing = !account.isEditing;
    });
  }
  account.isEditing = !account.isEditing;
}

FinancialController.prototype.deleteAccount = function(account) {
  var data = {csrfmiddlewaretoken: this.scope_.csrfToken};
  data = decodeURIComponent($.param(data));

  this.http_({
      method: 'POST',
      url: '/f/delete-account-' + account.pk + '/',
      data: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(function() {
      account.isDeleted = true;
    }, function() {
      alert('Failed to update account')
    });
}

FinancialController.prototype.addAccount = function() {
  var ctrl = this;
  var data = {name: this.newAccount.name,
      csrfmiddlewaretoken: this.scope_.csrfToken};

  data = decodeURIComponent($.param(data));

  this.http_({
    method: 'POST',
    url: '/f/insert-account/',
    data: data,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(function(response){
    var account = response.data[0];
    ctrl.accounts_.push(account);
    this.newAccount.name = '';
  }, function() {
    alert('Failed to update account')
    account.isEditing = !account.isEditing;
  });
}
