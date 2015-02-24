(function(_){
    angular.module('cooperativa.cxp',['ngAnimate'])

        .factory('cxpService',['$http','$q','$filter', function ($http, $q, $filter) {
            function getAll() {
                var deferred = $q.defer();

                $http.get('cxp/')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });

                return deferred.promise();
            }
            
            function getCxpsById(id){
                var deferred = $q.defer();
                
                getAll().then(function (data) {
                    var result =data.filter(function (reg){
                        reg.id = id; 
                       return reg;
                    });
                    if(result.length > 0){
                        deferred.resolve(result);
                    }else{
                        deferred.reject();
                    }
                });
                
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
                        reg.socioId=socioId;
                        return reg;
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
                        reg.suplidorId = supId;
                        return reg;
                    });

                    if(result.length > 0){
                        deferred.resolve(result);
                    }
                    else{
                        deferred.reject();
                    }
                });

            }

            function socios() {
                var deferred = $q.defer();

                $http.get('/api/socio/?format=json')
                  .success(function (data) {
                    deferred.resolve(data.filter( function(socio) {
                      return socio.estatus == "E" || socio.estatus == "S";

                    }));
                  });

            function suplidor(){
                var deferred =$q.defer();

                $http.get('api/suplidor/?format=json')
                .success(function (data){
                    deferred.resolve(data);})
                .error(function (err){
                    deferred.resource(err);
                });

            }

        return deferred.promise;
      }

            return {
                getAll: getAll,
                getCxpsById: getCxpsById,
                getCxpByDate: getCxpByDate,
                getCxpBySocio: getCxpBySocio,
                getCxpBySuplidor: getCxpBySuplidor,
                socios:socios,
                suplidor:suplidor
            };

        }])
        .controller('cxpController',['$scope', '$filter', '$rootScope', 'cxpService','$timeout',
            function($scope, $filter, $rootScope, cxpService, $timeout){
                $scope.cxpData=[];
                $scope.cxpFilterData=[];
                $scope.fechaI=null;
                $scope.fechaF=null;
                $scope.socioId=null;
                $scope.suplidorId=null;
                $scope.ArrowLF = 'UpArrow';
                $scope.showLF = true;
                $scope.getdate=$filter('date')(Date.now(),'dd/MM/yyyy');

                $scope.toggleLF= function(){
                    $scope().showLF = !$scope.showLF;

                   $scope.showLF = !$scope.showLF;

                    if($scope.showLF === true) {
                      $scope.ArrowLF = 'UpArrow';
                    } else {
                      $scope.ArrowLF = 'DownArrow';
                    }
                };

                  $scope.getSocio = function($event) {
                    $event.preventDefault();

                    $scope.tableSocio = true;

                    if($scope.socioNombre != undefined) {
                      FacturacionService.socios().then(function (data) {
                        $scope.socios = data.filter(function (registro) {
                          return $filter('lowercase')(registro.nombreCompleto
                                              .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
                        });

                        if($scope.socios.length > 0){
                          $scope.tableSocio = true;
                          $scope.socioNoExiste = '';
                        } else {
                          $scope.tableSocio = false;
                          $scope.socioNoExiste = 'No existe el socio';
                        }

                      });
                    } else {
                      FacturacionService.socios().then(function (data) {
                        $scope.socios = data;
                        $scope.socioCodigo = '';
                      });
                    }
                  }
                         //Seleccionar Socio
              $scope.selSocio = function($event, s) {
                $event.preventDefault();

                $scope.socioNombre = s.nombreCompleto;
                $scope.socioCodigo = s.codigo;
                $scope.tableSocio = false;
              }

                $scope.getAllData = function(){
                    $scope.cxpData=cxpService.getAll();
                };

                $scope.getCxpByDate = function(){
                    $scope.cxpFilterData=cxpService.getCxpByDate($scope.fechaI,$scope.fechaF);
                };

                $scope.getCxpSocio = function(){
                    $scope.cxpFilterData=cxpService.getCxpBySocio($scope.socioId);
                };

                $scope.getcxpSup = function(){
                    $scope.cxpFilterData= cxpService.getCxpBySuplidor($scope.idSuplidor);
                };

                                } ]
                                );
})(_);