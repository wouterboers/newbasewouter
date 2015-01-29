(function (angular) {
    'use strict';
    var app = angular.module('app', ['ngRoute']);

    app.config(['$interpolateProvider', function ($interpolateProvider) {
        $interpolateProvider.startSymbol('{[');
        $interpolateProvider.endSymbol(']}');
    }]);

    //app.controller('MainController', function ($scope, $route, $routeParams, $location) {
    //    $scope.$route = $route;
    //    $scope.$location = $location;
    //    $scope.$routeParams = $routeParams;
    //
    //    //$scope.reloadRoute = function () {
    //    // $route.reload();
    //    //};
    //})

    app.config(function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/', {
                templateUrl: '/projects',
                controller: 'ProjectsListCtrl',
                resolve: {}
            })
            .when('/projects', {
                templateUrl: 'projects',
                controller: 'ProjectsListCtrl',
                resolve: {}
            })
            .when('/project_edit', {
                templateUrl: 'project_edit',
                controller: 'UpdateProjectCtrl'
            })
            .otherwise({redirectTo: '/'});


        // configure html5 to get links working on jsfiddle
        $locationProvider.html5Mode(true);
    });

    app.controller('ProjectsListCtrl', function ($scope, $http) {
        $http.get('/main').success(function (data) {
            $scope.projects = data;
        });

        $scope.show = function ($e) {
            var $this = $($e.target).parent('div');

            $('.popup,.modal').fadeIn();
            var $id = $($this).attr('id');
            var $name = $($this).attr('name');

            $('.popup .modal input[name=name]').val($name);
            $('.popup .modal input[name=id]').val($id).attr("ng-init", "id='" + $id + "'");
        }
    });

    app.controller('MainMenu', function ($scope, $http) {
        $scope.hide_menu = function ($event) {
            $('.toggle_menu').toggle("slide");
            $('.ng_view_content').animate({left: 30}, 500);
        }
        $scope.call_menu = function ($event) {
            $('.toggle_menu').toggle("slide");
            $('.ng_view_content').animate({left: 300}, 500);
        }
    });

    app.controller('InsertProjectCtrl', function ($scope, $http) {
        $scope.insertProject = function () {
            $http.post('/main', {
                id: $scope.id,
                name: $scope.name,
                ind_selected: $scope.toggle
            })
        }
    });

    app.controller('UpdateProjectCtrl', function ($scope, $http) {
        $scope.updateProject = function () {
            $http.put('/main', {
                id: $scope.id,
                name: $scope.name,
                ind_selected: $scope.toggle
            }).success(function () {
                newbase.pop_up.close();
            })
        };

        $scope.close = function () {
            $('.popup, .modal').fadeOut();
        }
    });

})(window.angular);


var newbase = new function () {
    this.scope = new function () {
        this.onload = function () {
            $(function () {

                newbase.pop_up.show();
                newbase.pop_up.close();
            })
        };
        this.what_is_my_name = function ($a) {
            return ($a);
        }

    };

    this.pop_up = new function () {
        this.show = function ($this) {
            $('.popup').fadeIn();
            var $id = $($this).attr('id');
            var $name = $($this).attr('name');

            $('.popup .modal input[name=name]').val($name);
            $('.popup .modal input[name=id]').val($id).attr("ng-init", "id='" + $id + "'");
        };
        this.close = function () {
            $('body').delegate('.popup .close', 'click', function () {
                $('.popup').fadeOut();
            });
        }
    }
};
