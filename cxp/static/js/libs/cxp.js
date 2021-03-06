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

            function editOrden(Orden, Detalle, Eliminar){
                var deferred = $q.defer();
                
                $http.post('/cxp/edit/', JSON.stringify({'Orden': Orden, 'Detalle': Detalle, 'Eliminar': Eliminar}))
                    .success(function (data){
                        deferred.resolve(data);
                    })
                    .error(function (err){
                        deferred.resolve(err);
                    });
                return deferred.promise;
            }


            function editOrdenSuper(Orden, Detalle, Eliminar){
                var deferred = $q.defer();
                $http.post('/cxpSuper/edit/', JSON.stringify({'Orden': Orden, 'Detalle': Detalle, 'Eliminar': Eliminar}))
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
            };

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
            }; 

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
                solicitudOrden     : solicitudOrden,
                editOrden        : editOrden,
                editOrdenSuper   : editOrdenSuper

                
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
                $scope.btnDisable = false;
                $scope.valoresChk = [];
                $scope.reg = [];
                $scope.ordenSimple = [];
                $scope.detalleOrdenesEdit = [];
                $scope.ordenesSeleccionada = [];
                $scope.numReg =0;
                $scope.ordenesEliminar = [];



                
            $scope.nuevaOrden = function(){
                $scope.listCxp = false;
                $scope.crCxp = true;
                $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
                $scope.cxpDataReg.descuento = 0;

            };

            $scope.findOrden = function ($event){
               SolicitudOrdenDespachoService.solicitudesODForCXP().then(function (data) {
                       
                        $scope.ordenesDetalle = data.filter(function (reg){
                            
                            return reg.cxp == "E" && reg.codigoSuplidor == $scope.cxpDataReg.suplidorId
                        });

                        $scope.ordenesDetalle.forEach(function(reg){
                            var orden = { };
                            orden.fechaSolicitud = reg.fechaSolicitud;
                            orden.id = null;
                            orden.idRegistro = reg.id;
                            orden.noSolicitud= reg.noSolicitud;
                            orden.montoSolicitado = reg.montoSolicitado;
                            $scope.ordenSimple.push(orden);
                        });

                        $scope.numReg = $scope.ordenesDetalle.length;
                 });
            }

            $scope.editarOrden = function($event, cxp){
                $event.preventDefault();

                var RegFecha = cxp.fecha.split('-');
                var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
                var Rfecha = FechaFormat;

                $scope.cxpDataReg.id = cxp.id;
                $scope.cxpDataReg.fecha = Rfecha;
                $scope.fecha = Rfecha;
                $scope.cxpDataReg.suplidorId = cxp.suplidorId;
                $scope.suplidorNombre = cxp.suplidor;
                $scope.cxpDataReg.concepto = cxp.concepto;
                $scope.cxpDataReg.monto = cxp.monto;
                $scope.cxpDataReg.descuento = cxp.descuento;

                $scope.listCxp = false;
                $scope.crCxp = true;

                if(cxp.estatus == 'P'){
                    $scope.btnDisable = true;
                }

                else{
                    $scope.btnDisable = false;
                }

                $scope.findOrden($event);

                $scope.detalleOrdenesEdit = cxp.detalle;

                cxp.detalle.forEach(function (reg){
                    var orden = {};
                  
                    orden.fechaSolicitud = reg.fecha;
                    orden.id = reg.id;
                    orden.idRegistro = reg.idRegistro;
                    orden.noSolicitud= reg.factura;
                    orden.montoSolicitado = reg.monto;
                    
                    $scope.ordenSimple.push(orden);

                    var entero = parseInt(orden.idRegistro.valueOf());
                    $scope.reg[entero] = true;
                    $scope.valoresChk[entero] = true;

                    $scope.selectedReg(orden);

                });
            
            }

            $scope.limpiar = function(){
                $scope.listCxp = true;
                $scope.crCxp = false;
                $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
                $scope.cxpDataReg = {};
                $scope.cxpDataReg.descuento = 0;
                $scope.ordenSimple = [];
                $scope.detalleOrdenesEdit = [];
                $scope.ordenesSeleccionada = [];
                $scope.numReg =0;
                $scope.ordenesEliminar = [];
                $scope.ordenesDetalle = [];
                $scope.reg = [];
                $scope.valoresChk = [];

            }

            $scope.CxpOrdenEstatus = function($event,estatus){
                $event.preventDefault();

                $scope.flap = false;
                cxpService.postCxpOrden(estatus).then(function (data){
                    if(data == "Ok"){
                        $scope.getAllData();
                        notie.alert(1, 'El registro # '+estatus+' ha sido posteada', 3);

                    }else{
                         notie.alert(3, 'Ocurrio un error al intentar postear el registro # '+estatus+'.', 3);
                    }
                });
            }

            //Cuando se le de click a un checkbox de la lista
            $scope.selectedReg = function(iReg) {
                index = $scope.ordenSimple.indexOf(iReg);

                if ($scope.reg[$scope.ordenSimple[index].idRegistro] === true){
                  if(_.findWhere($scope.ordenesEliminar, {id : iReg.id})){
                    $scope.ordenesEliminar = _.without($scope.ordenesEliminar, _.findWhere($scope.ordenesEliminar, {id : iReg.id}));
                  }
                  $scope.ordenesSeleccionada.push($scope.ordenSimple[index]);

                }
                else{
                  if(_.findWhere($scope.detalleOrdenesEdit, {id : iReg.id})){
                    $scope.ordenesEliminar.push(iReg);
                  }
                  $scope.ordenesSeleccionada = _.without($scope.ordenesSeleccionada, _.findWhere($scope.ordenesSeleccionada, {idRegistro : iReg.idRegistro}));
                
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
                    total = total +  parseFloat(item.montoSolicitado);  
                    });
                
                if($scope.cxpDataReg.id == undefined){
                    $scope.cxpDataReg.id = null;

                    if((total - $scope.cxpDataReg.descuento) == $scope.cxpDataReg.monto){
                        cxpService.setOrden($scope.cxpDataReg, $scope.ordenesSeleccionada).then(function(data){
                        
                        if(data =="Ok"){
                            notie.alert(1, 'Cuenta por pagar registrada', 3);
                            $scope.limpiar();
                            $scope.getAllData();
                        }
                        else{
                            notie.alert(3, 'Ocurrio un error al intentar guardar el registro.', 3);
                            }
                        });
                    }
                    else {
                            notie.alert(3, 'El monto a pagar es diferente al total de la factura.', 3);
                        }
                }
                else{

                    if((total - $scope.cxpDataReg.descuento) == $scope.cxpDataReg.monto){
                        cxpService.editOrden($scope.cxpDataReg, $scope.ordenesSeleccionada, $scope.ordenesEliminar)
                            .then(function (data){

                                if(data =="Ok"){
                                    notie.alert(1, 'Cuenta por pagar registrada', 3);
                                    $scope.limpiar();
                                    $scope.getAllData();
                                }
                                else {
                                    notie.alert(3, 'Ocurrio un error al intentar guardar el registro.', 3);
                                   
                                    }

                                })

                    }
                    else {
                        notie.alert(3, 'El monto a pagar es diferente al total de factura', 3);
                        
                    }
                }
                // function editOrden(Orden, Detalle, Eliminar)

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
                        notie.alert(1, 'Fue creada la solicitud para el registro # '+id, 3);
                    }else{
                        notie.alert(3, 'Ha ocurrido un error al intentar generarl la solicitud.', 3);
                      
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
            $scope.btnDisable = false;
            $scope.ordenesSeleccionada = [];
            $scope.reg = [];
            $scope.valoresChk = [];
            $scope.ordenSimple = [];
            $scope.detalleOrdenesEdit = [];
            $scope.ordenesSeleccionada = [];
            $scope.numReg =0;
            $scope.ordenesEliminar = [];

            // InventarioService.allEntradasForCXP()

            $scope.getAllData = function(){
                try{
                    cxpService.getAllSuper().then(function (data){
                        var datar = data;
                        $scope.lstCxpOrden = datar;
                        console.log(data);
                    });
                    
                }  
                catch(ex){
                    console.log(ex);
                }
            
            };

            //Cuando se le de click a un checkbox de la lista
            
            $scope.selectedReg = function(iReg) {
                index = $scope.ordenSimple.indexOf(iReg);

                if ($scope.reg[$scope.ordenSimple[index].idRegistro] === true){
                  if(_.findWhere($scope.ordenesEliminar, {id : iReg.id})){
                    $scope.ordenesEliminar = _.without($scope.ordenesEliminar, _.findWhere($scope.ordenesEliminar, {id : iReg.id}));
                  }
                  $scope.ordenesSeleccionada.push($scope.ordenSimple[index]);

                }
                else{
                  if(_.findWhere($scope.detalleOrdenesEdit, {id : iReg.id})){
                    $scope.ordenesEliminar.push(iReg);
                  }
                  $scope.ordenesSeleccionada = _.without($scope.ordenesSeleccionada, _.findWhere($scope.ordenesSeleccionada, {idRegistro : iReg.idRegistro}));
                
                }
                console.log($scope.ordenesEliminar);
            
            };

            $scope.editarOrden = function($event, cxp){
                $event.preventDefault();

                $scope.cxSuperData = {};
                
                var RegFecha = cxp.fecha.split('-');
                var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
                var Rfecha = FechaFormat;

                $scope.cxSuperData.id = cxp.id;
                $scope.cxSuperData.fecha = Rfecha;
                $scope.fecha = Rfecha;
                $scope.cxSuperData.suplidorId = cxp.suplidorId;
                $scope.suplidorNombre = cxp.suplidor;
                $scope.cxSuperData.concepto = cxp.concepto;
                $scope.cxSuperData.monto = cxp.monto;
                $scope.cxSuperData.descuento = cxp.descuento;

                $scope.vwTablas = false;
                $scope.vwRegistro = true;

                if(cxp.estatus == 'P'){
                    $scope.btnDisable = true;
                }
                else{
                    $scope.btnDisable = false;
                }

                $scope.detalleOrdenesEdit = cxp.detalle;

                $scope.getInventario($event,cxp.suplidorId);

                cxp.detalle.forEach(function (reg){
                var orden = {};

                orden.id = reg.id;
                orden.fecha = reg.fecha;
                orden.idRegistro= reg.Registro;
                orden.totalGeneral = reg.monto;
                
                $scope.ordenSimple.push(orden);

                var entero = parseInt(orden.idRegistro.valueOf());
                $scope.reg[entero] = true;
                $scope.valoresChk[entero] = true;

                $scope.selectedReg(orden);



                });

            };


            $scope.getInventario = function($event, suplidor){
                $event.preventDefault();

                InventarioService.allEntradasForCXP().then(function (data){
                    
                    $scope.inventarios = data.filter(function (ret){
                        console.log(data);
                        return ret.codigoSuplidor == suplidor;
                     });

                    $scope.inventarios.forEach(function(reg){
                        var orden = { };

                        orden.fecha = reg.fecha;
                        orden.id = null;
                        orden.idRegistro = reg.id;
                        orden.totalGeneral = reg.totalGeneral.replace(',','');
                        $scope.ordenSimple.push(orden);
                    });

                        $scope.numReg = $scope.inventarios.length;
                });

            };

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
                        
                        notie.alert(1, 'El registro # '+estatus+' Ha sido posteada', 3);
                    }

                    else{
                        notie.alert(3, 'Ocurrio un error al intentar postear el registro # '+estatus+'.', 3);
                    }
                });
            
            };

            $scope.printRegistros = function($event,s){
                $event.preventDefault();
                
                s.titulo = "Cuentas Por Pagar SuperCoop";
                $window.sessionStorage['CxpsH'] = JSON.stringify(s);
                $window.sessionStorage['CxpsD'] = JSON.stringify(s.detalle);

                $window.open('/cxp/imp', target='_blank'); 
            
            };

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
                $scope.btnDisable = false;
                $scope.cxSuperData = {};
                $scope.super = null;
                $scope.valoresChk = [];
                $scope.ordenSimple = [];
                $scope.detalleOrdenesEdit = [];
                $scope.ordenesSeleccionada = [];
                $scope.numReg =0;
                $scope.ordenesEliminar = [];
                
                $scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
                
            };


            $scope.guardarCxp = function($event){
                $event.preventDefault();
                debugger;
                var total = 0;

                $scope.ordenesSeleccionada.forEach(function (data){
                    data.totalGeneral = data.totalGeneral.replace(',','');
                    total = total + parseFloat(data.totalGeneral);
                });

                if($scope.cxSuperData.id == undefined){
                    
                    $scope.cxSuperData.id = null;

                    var RegFecha = $scope.fecha.split('/');
                    var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
                    $scope.cxSuperData.fecha = FechaFormat;

                    if((total - $scope.cxSuperData.descuento) == $scope.cxSuperData.monto){
                     var result = cxpService.setSuper($scope.cxSuperData, $scope.ordenesSeleccionada).then(function (data){
                        
                        if(data == "Ok"){
                           $scope.limpiar($event);
                            notie.alert(1, 'Cuenta por pagar registrada', 3);
                        }else{
                            notie.alert(3, 'Ocurrio un error al intentar registrar la CXP.', 3);

                            console.log(data);
                        }
                    });
                    }else{
                        notie.alert(3, 'El monto a pagar es diferente al total de las facturas')

                }
                }
                else{
                      if((total - $scope.cxSuperData.descuento) == $scope.cxSuperData.monto){
                        var orden = $scope.cxSuperData;
                        var result = cxpService.editOrdenSuper($scope.cxSuperData, $scope.ordenesSeleccionada, $scope.ordenesEliminar).then(function (data){
                            
                            if(data == "Ok"){
                               $scope.limpiar($event);
                                notie.alert(1, 'Cuenta por pagar registrada', 3);
                            }else{
                                notie.alert(3, 'Ocurrio un error al intentar registrar la CXP.', 3);

                                console.log(data);
                            }
                    });
                    }else{
                        notie.alert(3, 'El monto a pagar es diferente al total de las facturas.', 3);
                       
                }
                }

            };
            

            $scope.setSolicitud = function($event,id){
                $event.preventDefault();

                cxpService.solicitudSuperCoop(id).then(function (data){
                    if(data == "Ok"){
                        $scope.getAllData();
                        
                        notie.alert(1, 'Fue creada la solicitud para el registro #'+id, 3);
                    }else{
                        console.log(data);
                        notie.alert(3, 'Ha ocurrido un error al intentar generar la solicitud.', 3);
                       
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
                        
                    }
                }]);
})(_);