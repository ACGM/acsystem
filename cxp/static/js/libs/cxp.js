(function(_){
    angular.module('cooperativa.cxp',['ngAnimate'])

        .factory('cxpService',['$http','$q','$filter', function ($http, $q, $filter) {
            
            function getAll() {
                var deferred = $q.defer();
                $http.get('/cxpOrdenJson/?format=json')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });
                return deferred.promise;
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
                return deferred.promise;
                
            }

            function getCxpByOrden(orden){
                var deferred = $q.defer();

                getAll().then(function (data){
                    var result = data.filter(function (reg){
                        return reg.orden == orden;

                    });
                    if(result.length > 0){
                        deferred.resolve(result);
                    }else{
                        deferred.reject();
                    }
                });
                return deferred.promise;
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
                return deferred.promise;
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
                return deferred.promise;

            }

            function socios() {
                var deferred = $q.defer();

                $http.get('/api/socio/?format=json')
                  .success(function (data) {
                    deferred.resolve(data.filter( function(socio) {
                      return socio.estatus == "E" || socio.estatus == "S";

                    }));
                  });
                  return deferred.promise;
            }

            function suplidor(){
                var deferred =$q.defer();

                $http.get('/api/suplidor/?format=json')
                .success(function (data){
                    deferred.resolve(data);})
                .error(function (err){
                    deferred.resource(err);
                });
                
                return deferred.promise;
            }

            function setOrden(Orden, Detalle){
                var deferred = $q.defer();

                $http.post('/cxpOrdenJson/', JSON.stringify({'Orden':Orden, 'Detalle':Detalle}))
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve(err);
                    });
                return deferred.promise;
            }

            function getOcSuplidor(Suplidor, FechaI, FechaF){
                var deferred = $q.defer();

                $http.get('/api/prestamos/solicitudes/od/suplidor/'+suplidor+'/'+FechaI+'/'+FechaF)
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve(err);
                    });
                return  deferred.promise;
            }

            function getOcFecha(FechaI, FechaF){
                var deferred = $q.defer();

                $http.get('/api/prestamos/solicitudes/od/fecha/'+FechaI+'/'+FechaF)
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve(err);
                    });

                return deferred.promise;
            }

            return {
                getAll: getAll,
                getCxpsById: getCxpsById,
                getCxpByDate: getCxpByDate,
                getCxpBySocio: getCxpBySocio,
                getCxpBySuplidor: getCxpBySuplidor,
                getCxpByOrden: getCxpByOrden,
                socios: socios,
                suplidor: suplidor,
                setOrden: setOrden,
                getOcSuplidor: getOcSuplidor,
                getOcFecha: getOcFecha
                
            };

        }])
        .controller('cxpController',['$scope', '$filter', '$rootScope', 'cxpService','$timeout', 'SolicitudOrdenDespachoService',
            function($scope, $filter, $rootScope, cxpService, $timeout, SolicitudOrdenDespachoService){
                $scope.cxpData = [];
                $scope.cxpDataDetalle = [];
                $scope.cxpDiario = [];
                $scope.cxpFilterData = [];
                $scope.cxpDataReg = null;
                $scope.fechaI = null;
                $scope.fechaF = null;
                $scope.socioId = null;
                $scope.suplidorId = null;
                $scope.tableSocio = false;
                $scope.ArrowLF = 'UpArrow';
                $scope.DetArrow = 'UpArrow';
                $scope.DatArrow = 'UpArrow';
                $scope.showDet = false;
                $scope.showLF = true;
                $scope.showDat = false;
                $scope.panelDetalleArt = false;
                $scope.DetallesArt =false;
                $scope.OrdenCrPanel = false;
                $scope.OrdenReg = false;
                $scope.OrdenList = true;
                $scope.getdate = false;
                $scope.selectSocio = null;
                $scope.tableOrden = false;
                $scope.detallesOrd={};

                
            $scope.nuevaOrden = function(){
                $scope.getdate = $filter('date')(Date.now(),'dd/MM/yyyy');
                $scope.OrdenList = false;
                $scope.OrdenCrPanel = true;
                $scope.panelDetalleArt = true;
                $scope.OrdenReg = true;
                $scope.DetallesArt = true;
                $scope.cxpFilterData = null;
                $scope.suplidorNombre = null;
                $scope.socioNombre = null;
                $scope.cxpDataDetalle = [];
                $scope.cxpDiario = [];
                $scope.detallesOrd = {};
                
            };

            $scope.toggleLF= function(){
             
               $scope.showLF = !$scope.showLF;

                if($scope.showLF === true) {
                  $scope.ArrowLF = 'UpArrow';
                } else {
                  $scope.ArrowLF = 'DownArrow';
                }

                if($scope.OrdenList === true){
                    $scope.OrdenList = false;
                }else{
                    $scope.OrdenList = true;
                }
            };

            $scope.toggleDt= function(){
        
               $scope.showDet = !$scope.showDet;

                if($scope.showDet === true) {
                  $scope.DetArrow = 'UpArrow';
                } else {
                  $scope.DetArrow = 'DownArrow';
                }

                if($scope.DetallesArt === true){
                    $scope.DetallesArt = false;
                }else{
                    $scope.DetallesArt = true;
                }
            };

            $scope.findOrden = function ($event){
                $scope.tableOrden = true;
               SolicitudOrdenDespachoService.solicitudesODForCXP().then(function (data) {
                        return data.filter(function (reg){
                            return reg.socios == $scope.cxpDataReg.socioId && reg.suplidor == $scope.cxpDataReg.suplidorId
                        });
                 });
            }

            $scope.toggleDat= function(){
                $scope.showDat = !$scope.showDat;

                if($scope.showDat === true) {
                    $scope.DatArrow = 'UpArrow';
                }else{
                    $scope.DatArrow = 'DownArrow';
                }

                if( $scope.OrdenReg  === true){
                     $scope.OrdenReg = false;
                }else{
                     $scope.OrdenReg = true;
                }
            };

            $scope.limpiar = function(){
                $scope.cxpData = [];
                $scope.cxpDataDetalle = [];
                $scope.cxpDiario = [];
                $scope.cxpFilterData = [];
                $scope.cxpDataReg =[];
                $scope.socioId = null;
                $scope.suplidorId = null;
                $scope.socioNombre = null;
                $scope.suplidorNombre = null;

            }

            $scope.guardarOrden = function($event){

                if($scope.cxpDataReg.id === undefined){
                    $scope.cxpDataReg.id = null;
                    $scope.cxpDataReg.estatus = 'A';
                    }
                else{
                    console.log($scope.cxpDataDetalle);
                }

                var RegFecha = $scope.cxpDataReg.fecha.split('/');
                var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
                $scope.cxpDataReg.fecha = FechaFormat;
               
                var result = cxpService.setOrden($scope.cxpDataReg, $scope.cxpDataDetalle);
                $scope.limpiar();
                $scope.OrdenList = false;
                $scope.OrdenCrPanel = true;
                $scope.panelDetalleArt = true;
                $scope.DetallesArt = true;
                $scope.OrdenReg = true;
                $scope.ArrowLF = 'DownArrow';

                console.log(result);    

            }

            $scope.getSuplidor = function($event){
                    $event.preventDefault();

                    $scope.tableSuplidor = true;
                    $scope.tableSocio = false;
                    if($scope.suplidorNombre !== undefined) {
                      cxpService.suplidor().then(function (data) {
                        $scope.suplidor = data.filter(function (registro) {
                           return $filter('lowercase')(registro.nombre
                                              .substring(0,$scope.suplidorNombre.length)) == $filter('lowercase')($scope.suplidorNombre);
                        });

                        if($scope.suplidor.length > 0){
                          $scope.tableSuplidor = true;
                          $scope.suplidorNoExiste = '';
                        } else {
                          $scope.tableSuplidor = false;
                          $scope.suplidorNoExiste = 'No existe el socio';
                        }

                      });
                    } else {
                      cxpService.suplidor().then(function (data) {
                        $scope.suplidor = data;
                        $scope.suplidorCodigo = '';
                      });
                    }
                  };
                  
            $scope.getSocio = function($event) {
                    $event.preventDefault();
                    $scope.tableSocio = true;
                    $scope.tableSuplidor = false;

                    if($scope.socioNombre !== undefined) {
                      cxpService.socios().then(function (data) {
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
                      cxpService.socios().then(function (data) {
                        $scope.socios = data;
                        $scope.socioCodigo = '';
                      });
                    }
                  };
                         //Seleccionar Socio
            
            $scope.selOrden = function($event, s) {
                $event.preventDefault();
                
                $scope.cxpDataReg.orden = s.noSolicitud ;
                $scope.ordenReg = s.noSolicitud+'-'+s.fechaSolicitud ;
                $scope.cxpDataReg.monto = s.monto;
                $scope.tableOrden = false;
                
              };

            $scope.selSocio = function($event, s) {
                $event.preventDefault();
                
                $scope.socioNombre = s.nombreCompleto;
                $scope.cxpDataReg.socioId = s.codigo;
                $scope.tableSocio = false;

                $scope.cxpDataReg.orden = null ;
                $scope.ordenReg = null ;
                $scope.cxpDataReg.monto = 0;
                
              };


            $scope.selSuplidor = function($event, s) {
                $event.preventDefault();

                $scope.suplidorNombre = s.nombre;
                $scope.cxpDataReg.suplidorId = s.id;
                $scope.tableSuplidor= false;

                $scope.cxpDataReg.orden = null ;
                $scope.ordenReg = null ;
                $scope.cxpDataReg.monto = 0;
              };

            $scope.getAllData = function(){
                try{
                    cxpService.getAll().then(function (data){
                        var datar = data;
                        $scope.cxpData = datar;
                    });
                    
                }  
                catch(ex){
                    console.log(ex);
                }
            
            };

            $scope.selOrdenById = function(id){
                cxpService.getCxpsById(id).then(function (data){
                    $scope.cxpDataReg = data[0];

                    $scope.suplidorNombre = $scope.cxpDataReg.suplidor;
                    $scope.socioNombre = $scope.cxpDataReg.socio;
                    $scope.cxpDataReg.fecha = $filter('date')($scope.cxpDataReg.fecha,'dd/MM/yyyy');
                    $scope.OrdenList = false;
                    $scope.OrdenCrPanel = true;
                    $scope.panelDetalleArt = true;
                    $scope.DetallesArt = true;
                    $scope.OrdenReg = true;
                    $scope.ArrowLF = 'DownArrow';
                                    });
            };

            $scope.getCxpByDate = function(){
                $scope.cxpFilterData=cxpService.getCxpByDate($scope.fechaI, $scope.fechaF);
            };

            $scope.getCxpSocio = function(){
                $scope.cxpFilterData=cxpService.getCxpBySocio($scope.socioId);
            };

            $scope.getcxpSup = function(){
                $scope.cxpFilterData= cxpService.getCxpBySuplidor($scope.idSuplidor);
            };

          
            }])

    .controller('CxpSuperCtrl', ['$scope', '$filter', '$rootScope', 'cxpService', '$timeout' 
        , function ($scope, $filter, $rootScope, cxpService, $timeout) {

      $scope.lstCxpOrden = []

        
    }]);
})(_);