/**
 * :copyright (c) 2014 - 2018, The Regents of the University of California, through Lawrence Berkeley National Laboratory (subject to receipt of any required approvals from the U.S. Department of Energy) and contributors. All rights reserved.
 * :author
 */
angular.module('BE.seed.controller.settings_profile_modal', [])
  .controller('settings_profile_modal_controller', [
    '$scope',
    '$uibModalInstance',
    'inventory_service',
    'action',
    'data',
    function ($scope, $uibModalInstance, inventory_service, action, data) {
      $scope.action = action;
      $scope.data = data;

      $scope.rename_profile = function () {
        if (!$scope.disabled()) {
          var id = $scope.data.id;
          var profile = _.omit($scope.data, 'id');
          profile.name = $scope.newName;
          inventory_service.update_settings_profile(id, profile).then(function (result) {
            $uibModalInstance.close(result.name);
          });
        }
      };

      $scope.remove_profile = function () {
        inventory_service.remove_settings_profile($scope.data.id).then(function () {
          $uibModalInstance.close();
        });
      };

      $scope.new_profile = function () {
        if (!$scope.disabled()) {
          inventory_service.new_settings_profile({
            name: $scope.newName,
            settings_location: 'List View Settings',
            columns: [{
              id: 674,
              pinned: Math.random() >= 0.5,
              order: 1
            }, {
              id: 676,
              pinned: Math.random() >= 0.5,
              order: 2
            }, {
              id: 678,
              pinned: Math.random() >= 0.5,
              order: 3
            }]
          }).then(function (result) {
            $uibModalInstance.close(result);
          });
        }
      };

      $scope.disabled = function () {
        if ($scope.action === 'rename') {
          return _.isEmpty($scope.newName) || $scope.newName === $scope.data.name;
        } else if ($scope.action === 'new') {
          return _.isEmpty($scope.newName);
        }
      };

      $scope.cancel = function () {
        $uibModalInstance.dismiss();
      };
    }]);
