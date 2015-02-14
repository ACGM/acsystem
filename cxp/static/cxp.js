(function(){
    angular.module('cooperativa.cxp',[ngAnimate])

        .factory('cxpService','$http','$q','$filter', function ($http, $q, $filter) {
            function getAll() {
                var deferred = $q.defer();

                $http.get('cxp/')
                    .success(function (data) {
                        deferred.resolve(data)
                    })
                    .error(function (data) {
                        deferred.resolve(data)
                    });

                return deferred.promise();
            }
            
            function getCxpsById(id){
                var deferred = $q.defer();
                
                getAll().then(function (data) {
                    var result =data.filter(function (reg){
                       return reg.id = id;
                    });
                    if(result.length > 0){
                        deferred.resolve(result);
                    }else{
                        deferred.reject();
                    }
                })
                
            }

            function getCxpByDate(DateI, DateF){
                var deferred = $q.defer();

                getAll().then(function  (data){
                    var result=data.filter(function(reg){
                        return reg.fecha >= DateI && reg.fecha <=DateF;
                    });

                    if(result.length>0){
                        deferred.resolve(result);
                    }
                    else{
                        deferred.reject();
                    }
                });
            }

            function getCxpBySocio(socioId){
                var deferred=$q.defer();

                getAll().then(function (data){
                    var result = data.filter(function (reg){
                        return reg.socioId=socioId;
                    });

                    if(result.length > 0){
                        deferred.resolve(result);
                    }
                    else{
                        deferred.reject();
                    }
                });
            }

            function getCxpBySuplidor(supId){
                var deferred = $q.defer();

                getAll().then(function (data){
                    var result = data.filter(function (reg){
                        return reg.suplidorId = supId;
                    });

                    if(result.length > 0){
                        deferred.resolve(result);
                    }
                    else{
                        deferred.reject();
                    }
                });
            }

            return {
                getAll: getAll,
                getCxpsById: getCxpsById,
                getCxpByDate: getCxpByDate,
                getCxpBySocio: getCxpBySocio,
                getCxpBySuplidor: getCxpBySuplidor
            }

        }
            )
        .controller('cxpController',['$scope', '$filter', '$rootScope', 'cxpServices','$timeout',
            function($scope, $filter, $rootScope, cxpService, $timeout){
                $scope.cxpData=[];
                $scope.cxpFilterData=[];
                $scope.fechaI=null;
                $scope.fechaF=null;
                $scope.socioId=null;
                $scope.suplidorId=null;

                $scope.getAllData = function(){
                    $scope.cxpData=cxpService.getAll();
                }

                $scope.getCxpByDate = function(){
                    $scope.cxpFilterData=cxpService.getCxpByDate($scope.fechaI,$scope.fechaF);
                }

                $scope.getCxpSocio = function(){
                    $scope.cxpFilterData=cxpService.getCxpBySocio($scope.socioId);
                }

                $scope.getcxpSup = function(){
                    $scope.cxpFilterData= cxpService.getCxpBySuplidor($scope.idSuplidor);
                }

                                } ])
})(_);