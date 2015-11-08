(function(_){
    angular.module('cooperativa.cxp',['ngAnimate'])

        .filter('estatusCxp', function() {
          return function (input) {
            if (!input) return "";

            input = input
                    .replace('P', 'Posteada')
                    .replace('A', 'Activa')
                    .replace('N', 'Nula');
                return input;
             }
        })
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

             function getAllSuper() {
                var deferred = $q.defer();
                $http.get('/cxpSuperJson/?format=json')
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

            function setSuper(regSuper, Detalle){
                var deferred = $q.defer();

                $http.post('/cxpSuperJson/', JSON.stringify({'regSuper':regSuper, 'Detalle': Detalle}))
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

            function postCxpOrden(orden){
                var deferred = $q.defer();

                $http.post('/cxp/cxpOrden/?orden='+orden).
                    success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve (err);
                    });

                return deferred.promise;
            };

            function postCxpSuper(orden){
                var deferred = $q.defer();

                $http.post('/cxp/superOrden/?super='+orden)
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve (err);
                    });

                return deferred.promise;
            };//cxp/solicitud/supercoop/

            function solicitudSuperCoop(orden){
                var deferred = $q.defer();

                $http.post('/cxp/solicitud/supercoop/?super='+orden)
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve (err);
                    });

                return deferred.promise;
            }; //cxp/solicitud/ordenCompra/

            function solicitudOrden(orden){
                var deferred = $q.defer();

                $http.post('/cxp/solicitud/ordenCompra/?orden='+orden)
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve (err);
                    });

                return deferred.promise;
            };

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
                getOcFecha: getOcFecha,
                postCxpOrden : postCxpOrden,
                getAllSuper : getAllSuper,
                postCxpSuper: postCxpSuper, 
                setSuper    : setSuper,
                solicitudSuperCoop : solicitudSuperCoop,
                solicitudOrden     : solicitudOrden

                
            };

        }])
        .controller('cxpController',['$scope', '$filter', '$rootScope', 'cxpService','$timeout', 'SolicitudOrdenDespachoService','$window',
            function($scope, $filter, $rootScope, cxpService, $timeout, SolicitudOrdenDespachoService, $window){
                $scope.cxpData = [];
                $scope.cxpDataDetalle = [];
                $scope.cxpDiario = [];
                $scope.cxpFilterData = [];
                $scope.ordenesDetalle = [];
                $scope.cxpDataReg = {};
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
                $scope.ROrden  = [];
                $scope.flap = false;
                $scope.crCxp = false;
                $scope.listCxp = true;
                $scope.valoresChk = [];
                $scope.reg = [];
                $scope.ordenesSeleccionada = [];



                
            $scope.nuevaOrden = function(){
                $scope.listCxp = false;
                $scope.crCxp = true;
                $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
                $scope.cxpDataReg.descuento = 0;

            };

            $scope.findOrden = function ($event){
               SolicitudOrdenDespachoService.solicitudesODForCXP().then(function (data) {
                        console.log(data);
                        $scope.ordenesDetalle = data.filter(function (reg){
                            
                            return reg.cxp == "E" && reg.codigoSuplidor == $scope.cxpDataReg.suplidorId
                        });
                        
                 });
            }

            $scope.limpiar = function(){
                $scope.listCxp = true;
                $scope.crCxp = false;
                $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
                $scope.cxpDataReg = {};
                $scope.cxpDataReg.descuento = 0;

            }

            $scope.CxpOrdenEstatus = function($event,estatus){
                $event.preventDefault();

                $scope.flap = false;
                cxpService.postCxpOrden(estatus).then(function (data){
                    if(data == "Ok"){
                        $scope.getAllData();
                        alert("La orden # "+estatus+" Ha sido posteada");

                    }else{
                         alert("Ocurrio un error al intentar guardar la orden");
                    }
                });


            }

                 //Cuando se le de click a un checkbox de la lista
              $scope.selectedReg = function(iReg) {
                index = $scope.ordenesDetalle.indexOf(iReg);

                if ($scope.reg[$scope.ordenesDetalle[index].id] === true){
                  $scope.ordenesSeleccionada.push($scope.ordenesDetalle[index]);
                  console.log($scope.ordenesSeleccionada);
                }
                else{
                  $scope.ordenesSeleccionada = _.without($scope.ordenesSeleccionada, _.findWhere($scope.ordenesSeleccionada, {id : iReg.id}));
                   console.log($scope.ordenesSeleccionada);
                }
              }

            $scope.printRegistros = function($event,s){
                $event.preventDefault();
                
                s.titulo = "Cuentas Por Pagar Ordenes";
                $window.sessionStorage['CxpsH'] = JSON.stringify(s);
                $window.sessionStorage['CxpsD'] = JSON.stringify(s.detalle);

                $window.open('/cxp/imp', target='_blank'); 
            }

            $scope.guardarOrden = function($event){

                var total = 0;

                var RegFecha = $scope.fecha.split('/');
                var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
                var Rfecha = FechaFormat;
                     
                $scope.cxpDataReg.fecha = Rfecha;
                $scope.ordenesSeleccionada.forEach(function (item) {
                    total = total +  parseFloat(item.netoDesembolsar);  
                });

                if((total - $scope.cxpDataReg.descuento) == $scope.cxpDataReg.monto){
                    cxpService.setOrden($scope.cxpDataReg, $scope.ordenesSeleccionada).then(function(data){
                        if(data =="Ok"){
                            alert("Cuenta por pagar Registrada")
                            $scope.limpiar();
                            $scope.getAllData();
                        }else{
                            alert("Ocurrio un error al intentar guardar el registro")
                        }
                    });
                }else{
                    alert("El monto a pagar es diferente al total de factura");
                }

                // if($scope.cxpDataReg.id === undefined){
                //     $scope.cxpDataReg.id = null;
                //     $scope.cxpDataReg.estatus = 'A';
                //     }
                // else{
                //     console.log($scope.cxpDataDetalle);
                // }

                // var RegFecha = $scope.cxpDataReg.fecha.split('/');
                // var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
                // $scope.cxpDataReg.fecha = FechaFormat;
               
                // var result = cxpService.setOrden($scope.cxpDataReg, $scope.cxpDataDetalle);
                // $scope.limpiar();
                // $scope.OrdenList = false;
                // $scope.OrdenCrPanel = true;
                // $scope.panelDetalleArt = true;
                // $scope.DetallesArt = true;
                // $scope.OrdenReg = true;
                // $scope.ArrowLF = 'DownArrow';

                // $scope.getAllData();

            };

            $scope.workflow = function($event, id){
                $event.preventDefault();
                
                $scope.orden = id;
                $scope.flap = true;
            };

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


            $scope.selOrden = function($event, s) {
                $event.preventDefault();
                
                $scope.cxpDataReg.orden = s.noSolicitud ;
                $scope.ordenReg = s.noSolicitud+'-'+s.fechaSolicitud ;
                $scope.cxpDataReg.monto = s.netoDesembolsar;
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

                $scope.findOrden($event);
              };


            $scope.getAllData = function(){
                try{
                    cxpService.getAll().then(function (data){
                        var datar = data;
                        $scope.cxpData = datar;
                        console.log(data);
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
    
            $scope.setSolicitud = function($event,id){
                $event.preventDefault();

                cxpService.solicitudOrden(id).then(function (data){
                    if(data == "Ok"){
                        $scope.getAllData();
                        alert("Fue creada la solicitud para la orden #"+id);
                    }else{
                        console.log(data);
                        alert("Ha ocurrido un error al intentar generar la solicitud");
                    }
                });
            };
        }])

        .controller('CxpSuperCtrl', ['$scope', '$filter', '$rootScope', 'cxpService', '$timeout', 'InventarioService', '$window',
            function ($scope, $filter, $rootScope, cxpService, $timeout, InventarioService, $window){

            $scope.lstCxpOrden = [];
            $scope.tableSuplidor = false;
            $scope.cxSuperData = {};
            $scope.suplidorNombre = null;
            $scope.inventarios = [];
            $scope.super = null;
            $scope.flap = false;
            $scope.fecha =$filter('date')(Date.now(),'dd/MM/yyyy');
            $scope.vwTablas = true;
            $scope.vwRegistro = false;
            $scope.ordenesSeleccionada = [];
            $scope.reg = [];

            // InventarioService.allEntradasForCXP()

            $scope.getAllData = function(){
                try{
                    cxpService.getAllSuper().then(function (data){
                        var datar = data;
                        $scope.lstCxpOrden = datar;
                    });
                    
                }  
                catch(ex){
                    console.log(ex);
                }
                };

                //Cuando se le de click a un checkbox de la lista
            $scope.selectedReg = function(iReg) {
                index = $scope.inventarios.indexOf(iReg);

                if ($scope.reg[$scope.inventarios[index].id] === true){
                  $scope.ordenesSeleccionada.push($scope.inventarios[index]);
                  console.log($scope.ordenesSeleccionada);
                }
                else{
                  $scope.ordenesSeleccionada = _.without($scope.ordenesSeleccionada, _.findWhere($scope.ordenesSeleccionada, {id : iReg.id}));
                   console.log($scope.ordenesSeleccionada);
                }
              }


            $scope.getInventario = function($event, suplidor){
                $event.preventDefault();

                InventarioService.allEntradasForCXP().then(function (data){
                    console.log(data)
                    $scope.inventarios = data.filter(function (ret){
                        return ret.codigoSuplidor == suplidor;
                     });
                });



            }

            $scope.nuevoRegistro = function(){
                $scope.cxSuperData = {};
                $scope.vwTablas = false;
                $scope.vwRegistro = true;
                $scope.cxSuperData.descuento = 0;
                };


            $scope.selSuplidor = function($event, s) {
                $event.preventDefault();
                
                $scope.suplidorNombre = s.nombre;
                $scope.cxSuperData.suplidorId = s.id;
                $scope.tableSuplidor= false;

                $scope.getInventario($event, s.id);


              };


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
                              $scope.suplidorNoExiste = 'Suplidor no existe';
                            }
                             
                          });
                        } else {
                          cxpService.suplidor().then(function (data) {
                            $scope.suplidor = data;
                            $scope.suplidorCodigo = '';
                          });
                        }
                      };


            $scope.CxpSuperEstatus = function($event,estatus){
                $event.preventDefault();

               
                cxpService.postCxpSuper(estatus).then(function (data){
                    
                    if(data == "Ok"){
                        $scope.getAllData();
                        alert("La orden # "+estatus+" Ha sido posteada");
                    }

                    else{
                         alert("Ocurrio un error al intentar postear la orden");
                    }
                });
                }
            $scope.printRegistros = function($event,s){
                $event.preventDefault();
                
                s.titulo = "Cuentas Por Pagar SuperCoop";
                $window.sessionStorage['CxpsH'] = JSON.stringify(s);
                $window.sessionStorage['CxpsD'] = JSON.stringify(s.detalle);

                $window.open('/cxp/imp', target='_blank'); 
            }

            $scope.workflow = function($event,id){
                $event.preventDefault();
                
                $scope.super = id;
                $scope.flap = true;
                };


            $scope.limpiar = function($event){
                $event.preventDefault();

                $scope.vwTablas = true;
                $scope.vwRegistro = false;

                $scope.getAllData();
                $scope.tableSuplidor = false;
                $scope.cxSuperData = {};
                $scope.super = null;
                
                $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
                
                };


            $scope.guardarCxp = function($event){
                $event.preventDefault();
                

                var RegFecha = $scope.fecha.split('/');
                var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
                $scope.cxSuperData.fecha = FechaFormat;
                
                var total = 0;

                $scope.ordenesSeleccionada.forEach(function (data){
                    data.totalGeneral = data.totalGeneral.replace(',','');
                    total = total + parseFloat(data.totalGeneral);
                });
                console.log($scope.ordenesSeleccionada);
               
                if((total - $scope.cxSuperData.descuento) == $scope.cxSuperData.monto){
                     var result = cxpService.setSuper($scope.cxSuperData, $scope.ordenesSeleccionada).then(function (data){
                    if(data == "Ok"){
                       $scope.limpiar($event);
                        alert("CxP Creada")
                    }else{
                        alert("Ocurrio un error al intentar registrar la CXP")
                        console.log(data);
                    }
                });
                }else{
                    alert("El monto a pagar es diferente al total de factura")
                }

                };
            

            $scope.setSolicitud = function($event,id){
                $event.preventDefault();

                cxpService.solicitudSuperCoop(id).then(function (data){
                    if(data == "Ok"){
                        alert("Fue creada la solicitud para el registro #"+id);
                    }else{
                        console.log(data);
                        alert("Ha ocurrido un error al intentar generar la solicitud");
                    }
                });
            };

            }])
        
        .controller('cxpImpController', ['$scope', '$filter', '$rootScope', 'cxpService', '$timeout' , '$window',
                function($scope, $filter, $rootScope, cxpService, $timeout, $window){
                    $scope.registro = [];
                    $scope.registroDetalle = [];
                    $scope.tipo = null;
                    $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');


                    $scope.inializar = function(){
                        $scope.registro = JSON.parse($window.sessionStorage['CxpsH']);
                        $scope.registroDetalle = JSON.parse($window.sessionStorage['CxpsD']);
                        console.log($scope.registro);
                    }
                }]);
})(_);