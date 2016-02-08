(function(_){
	 angular.module('cooperativa.contabilidad',['ngAnimate'])

        .factory('ContabilidadService', ['$http','$q','$filter', function ($http, $q, $filter) {
        	 
        	function getDiario() {
                var deferred = $q.defer();

                $http.get('/cuentasJson/?format=json')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                    	
                        deferred.resolve(data);
                    });
                return deferred.promise;
            }

            function getCuentasReg(){
            	var deferred = $q.defer();

            	$http.get('/api/cuentas/?format=json')
            		.success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });
                 return deferred.promise;
            }

            function getAuxiliar(){
            	var deferred = $q.defer();

                $http.get('/api/auxiliar/?format=json')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                        deferred.resolve(data);
                    });
                 return deferred.promise;
            }

            function getMayor(){
            	var deferred = $q.defer();

                $http.get('/contabilidad/Maestro_json/?format=json')
                    .success(function (data) {
                        deferred.resolve(data);
                    })
                    .error(function (data) {
                    	
                        deferred.resolve(data);
                    });
                return deferred.promise;
            }

            function getMayorByDate(FechaI, FechaF){
            	var deferred = $q.defer();

            	getMayor().then(function (data){
            		var FDesde =  FechaI.split("/");
            		var FHasta =  FechaF.split("/");

            		var result = data.filter(function (reg){
                        return new Date(reg.fecha.split("-")[0],parseInt(reg.fecha.split("-")[1])-1,reg.fecha.split("-")[2]) 
                            >= new Date(FDesde[2], parseInt(FDesde[1])-1, FDesde[0]) 
                            &&  new  Date(reg.fecha.split("-")[0],parseInt(reg.fecha.split("-")[1])-1,reg.fecha.split("-")[2]) 
                            <= new Date(FHasta[2], parseInt(FHasta[1])-1, FHasta[0])
                        });

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else {
            			deferred.resolve(result);
            		}
            	});
            	return	deferred.promise;
            }

            function getEstadoResultadoData(fechaI, fechaF){
            	var deferred = $q.defer();

            	$http.get('/contabilidad/EstResultado?format=json&&fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
            		.success(function (data){
            			deferred.resolve(data);
            		})
            		.error(function (err){
            			deferred.resolve(err);
            		});

            	return deferred.promise;

            }

            function getMayorByCuenta(FechaI, FechaF, Cuenta){
            	var deferred = $q.defer();

            	getMayorByDate(FechaI, FechaF).then(function (data){
            		var result = data.filter(function (reg){
            			return reg.cuenta == Cuenta;
            		});
					
					if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.resolve(result);
            		}
            	});
            	return	deferred.promise;

            }

            function getDiarioByFecha(FechaI, FechaF) {
            	var deferred = $q.defer();
            	
            	getDiario().then(function (data){
            		var FDesde =  FechaI.split("/");
            		var FHasta =  FechaF.split("/");

            		var result = data.filter(function (reg){
                           
                        return new Date(reg.fecha.split("-")[0],parseInt(reg.fecha.split("-")[1])-1,reg.fecha.split("-")[2]) 
                            >= new Date(FDesde[2], parseInt(FDesde[1])-1, FDesde[0]) 
                            &&  new  Date(reg.fecha.split("-")[0],parseInt(reg.fecha.split("-")[1])-1,reg.fecha.split("-")[2]) 
                            <= new Date(FHasta[2], parseInt(FHasta[1])-1, FHasta[0])
                        
                    });
                    
          

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.resolve(result);
            		}
            	});
            	return	deferred.promise;
            }

            function getDiarioByCuenta(FechaI, FechaF, cuenta){
            	var deferred = $q.defer();
              
            	getDiarioByFecha(FechaI, FechaF).then(function (data){
            		var result = data.filter(function (reg){
                        return reg.cuenta ==cuenta; 
                    });
            		if(result.length > 0){
            			deferred.resolve(result);
            		}else{
            			deferred.reject();
            		}
            	});
                return deferred.promise;
            }

            function getDiarioByAuxiliar(FechaI, FechaF, aux){
            	var deferred = $q.defer();

            	getDiario().then(function (data){
            		var result = data.filter(function (reg){
                        return reg.auxiliar == aux;
                    });

            		if (result.length > 0){
            			deferred.resolve(result);
            		}
            		else{
            			deferred.reject();
            		}

            	});
                  return deferred.promise;

            }

            function getDocumento(){
            	var deferred = $q.defer();

            	$http.get('/contabilidad/DiarioGeneral/?format=json')
            		.success(function (data) {
            			deferred.resolve(data);
            		})
            		.error(function (err) {
            			deferred.resolve(err);
            		})

            	return deferred.promise;
            }

	        //Guardar Registros en Diario General.
		    function guardarEnDiario(fecha, cuenta, ref, debito, credito) {
		        var deferred = $q.defer();

		        var doc = new Object();
		        doc.fecha = $filter('date')(fecha, 'yyyy-MM-dd');
		        doc.codCuenta = cuenta;
		        doc.ref = ref;
		        doc.estatus = 'P';
		        doc.debito = parseFloat(debito) > 0? debito.replaceAll(',','') : 0;
		        doc.credito = parseFloat(credito) > 0? credito.replaceAll(',','') : 0;

		        console.log('Debito: ' + debito);
		        console.log('Credito: ' + credito);
				console.log(doc)

		        $http.post('/contabilidad/RegDiario/', JSON.stringify({'cuenta': doc})).
		          success(function (data) {
		            deferred.resolve(data);
		          }).
		          error(function (data) {
		            deferred.resolve(data);
		          });
		        return deferred.promise;
		      }

            return {
            	getDiario : getDiario,
            	getDiarioByFecha : getDiarioByFecha,
            	getDiarioByCuenta : getDiarioByCuenta,
            	getDiarioByAuxiliar : getDiarioByAuxiliar,
            	getCuentasReg : getCuentasReg,
            	getAuxiliar : getAuxiliar,
            	getMayor : getMayor,
            	getMayorByDate : getMayorByDate,
            	getMayorByCuenta : getMayorByCuenta,
            	guardarEnDiario : guardarEnDiario,
            	getDocumento	: getDocumento,
            	getEstadoResultadoData : getEstadoResultadoData

				};
            }])

        .controller('ContabilidadController', ['$scope','$filter', '$rootScope', 'ContabilidadService','$timeout', '$window',
        					function ($scope, $filter, $rootScope, ContabilidadService, $timeout, $window) {
        						var date = new Date();

						        $scope.diario = [];
						        $scope.cuenta = null;
						        $scope.aux = null;
						        $scope.cuentas = null;
						        $scope.SFechaI = $filter('date')(new Date(date.getFullYear(), date.getMonth(),1),'dd/MM/yyyy');
						        $scope.SFechaF = $filter('date')(new Date(date.getFullYear(), date.getMonth(),28),'dd/MM/yyyy');
						        $scope.totalCredito = 0;
						        $scope.totalDebito = 0;
						        $scope.panelTotal ="total-compensado"
						        $scope.tipoDoc= [];
						        $scope.doc = null;

						        $scope.getAll = function(data){
						            ContabilidadService.getDiario().then(function (data){
						                 $scope.diario = data;
						                 console.log(data);
						                 $scope.calTotales();
						            });
						              
						        };

						        $scope.getByDate = function(){
						        	try{

						        		  ContabilidadService.getDiarioByFecha($scope.SFechaI, $scope.SFechaF).then(function (data){
						                    if(data.length > 0){
						                    	console.log(data)
						                        $scope.diario = data.sort(function(a, b){return b-a});
						                        $scope.calTotales();
						                    }else{
						                        $scope.diario=[];
						                        $scope.calTotales();
						                    }
						                  });
						        	}catch(ex){
						                    $scope.diario=[];
						                    $scope.calTotales();
						        	}

						        };

						        $scope.getDocs = function(){
						        	ContabilidadService.getDocumento().then(function (data){
						        		
						        		$scope.tipoDoc = data;
						        		console.log(data);
						        	});
						        };

						        $scope.filtDoc = function(){

						        	var codigo = $scope.doc.codigo;

						        	$scope.diario = $scope.diario.filter(function (data){
						        		return data.ref.match(codigo)
						        	});
						        	$scope.calTotales();
						        }

						        $scope.Clear = function(){

						             $scope.SFechaI = $filter('date')(new Date(date.getFullYear(), date.getMonth(),1),'dd/MM/yyyy');
						             $scope.SFechaF = $filter('date')(new Date(date.getFullYear(), date.getMonth(),28),'dd/MM/yyyy');
						             $scope.SAux = null;
						             $scope.SCuenta = null;
						             $scope.totalCredito = 0;
						             $scope.totalDebito = 0;
						             $scope.FillResult();
						        };

						        $scope.getByAux = function(){
						            try{
						                ContabilidadService.getDiarioByAuxiliar($scope.SFechaI, $scope.SFechaF, $scope.SAux).then(function (data){
						                   if(data.length > 0) {
						                        $scope.diario = data;
						                        $scope.calTotales();
						                    }else{
						                        $scope.diario=[];
						                        $scope.calTotales();
						                    }
						                });
						            }
						            catch(ex){
						                $scope.diario = [];
						                $scope.calTotales();
						                console.log(ex);
						            }
						        };

						        $scope.getByCuenta = function (){
						            try{
						                ContabilidadService.getDiarioByCuenta($scope.SFechaI, $scope.SFechaF, $scope.SCuenta).then(function (data){
						                   if(data.length > 0){
						                        $scope.diario = data.sort(function(a, b){return b-a});
						                        $scope.calTotales();
						                   }else{
						                        $scope.diario = data.sort(function(a, b){return b-a});;
						                        $scope.calTotales();
						                   }
						                    
						                });
						            }
						            catch(ex){
						                $scope.diario =[];
						                $scope.calTotales();
						                console.log(ex);
						            }
						        };

						        $scope.FillResult = function(){
						        	$scope.getDocs();
						            if($scope.SCuenta != undefined){
						                 $scope.getByCuenta();
						             }else if($scope.SAux != undefined){
						                 $scope.getByAux(); 
						             }else {
						                 $scope.getByDate();
						             }

						            $scope.calTotales();
						        }

						        $scope.getCuenta = function($event){
						        	$event.preventDefault();
						        	
						        	$scope.tableCuentas = true;
						        	$scope.tableAux = false;
						        	if($scope.SCuenta !== undefined) {
						                ContabilidadService.getCuentasReg().then(function (data){
						                    $scope.cuentas = data.filter(function (reg){
						                        return reg.codigo.toString().substring(0,$scope.SCuenta.length) == $scope.SCuenta;
						                    });
						                    if($scope.cuentas.length >0){
						                        $scope.tableCuentas = true;
						                        $scope.cuentaNoExiste = "";
						                    }else{
						                        $scope.tableCuentas = false;
						                        $scope.cuentaNoExiste = "No existe esta cuenta";
						                    }
						                });
						            } else {
						               ContabilidadService.getCuentasReg().then(function (data){	
						                $scope.cuentas = data;
						                $scope.cuentaNoExiste = ''; 

						              });
						            }

						        };

						        $scope.calTotales = function(){
						            $scope.totalDebito = 0;
						            $scope.totalCredito = 0;
						            if($scope.diario.length>0){

						                for (x = 0; x < $scope.diario.length; x ++){
						                    $scope.totalDebito = $scope.totalDebito + parseFloat($scope.diario[x].debito);
						                    $scope.totalCredito = $scope.totalCredito + parseFloat($scope.diario[x].credito);
						                }
						                if(parseFloat($scope.totalCredito) == parseFloat($scope.totalDebito)){
						                    $scope.panelTotal ="total-compensado"
						                }else{
						                    $scope.panelTotal ="total-noCompensado"
						                }
						            }
						        }

						        $scope.ImprimirRegistro = function($event){
						        	$event.preventDefault();

								    $window.print();
						        	
						        };

						        $scope.getAux = function($event){
						            $event.preventDefault();
						            
						            $scope.tableCuentas = false;
						            $scope.tableAux = true;
						            if($scope.SAux !== undefined) {
						                ContabilidadService.getAuxiliar().then(function (data){
						                    $scope.aux = data.filter(function (reg){
						                        return reg.codigo.toString().substring(0,$scope.SAux.length) == $scope.SAux;
						                    });
						                    if($scope.aux.length >0){
						                        $scope.tableCuentas = true;
						                        $scope.cuentaNoExiste = "";
						                    }else{
						                        $scope.tableCuentas = false;
						                        $scope.auxNoExiste = "No existe esta cuenta";
						                    }
						                });
						            } else {
						               ContabilidadService.getAuxiliar().then(function (data){    
						                $scope.aux = data;
						                $scope.SCueauxNoExistenta = ''; 
						              });
						            }

						        };

						        $scope.selCuenta = function($event, s) {
						                $event.preventDefault();
						                $scope.SCuenta = s.codigo;
						                $scope.tableCuentas = false;
						              };


						        $scope.selAux = function($event, s) {
						                $event.preventDefault();
						                $scope.SAux = s.codigo;
						                $scope.tableAux = false;
						              };
						        	
						     	}]
						    )
		
		.controller('EstadoRController', ['$scope','$filter', 'ContabilidadService', '$window' 
					,function ($scope, $filter, ContabilidadService, $window) {
			
			$scope.fechaI = null;
			$scope.fechaF = null;
			$scope.cabeceras = [];

			$scope.getDate = function(){
				var date = new Date();
				var dateI = new Date(date.getFullYear(), date.getMonth(), 1)
				var dateF = new Date(date.getFullYear(), date.getMonth() + 1, 0);

				$scope.fechaI = $filter('date')(dateI,'dd/MM/yyyy');
				$scope.fechaF = $filter('date')(dateF,'dd/MM/yyyy');
			};

			$scope.getData = function(){
				var RegFecha = $scope.fechaI.split('/');
		      	var fechaI = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
				
				var RegFecha1 = $scope.fechaF.split('/');
		      	var fechaF = RegFecha1[2] + '-' + RegFecha1[1] + '-' + RegFecha1[0];


				ContabilidadService.getEstadoResultadoData(fechaI, fechaF).then( function (data){
					
					var cuerpo = [];

					function compare(a,b) {
					  if (a.nivel < b.nivel)
					    return -1;
					  else if (a.nivel > b.nivel)
					    return 1;
					  else 
					    return 0;
					}

					$scope.cabeceras = data.filter( function (reg){
						return reg.nivel == 1;
					});
					
					var niv2 = data.filter( function (reg){
						return (reg.tipo == 'G' && reg.nivel > 1);
					});


					var detalle = data.filter( function (reg){
						
						return reg.tipo == 'D';
					});
					
					var result = null;


					niv2.forEach(function (regPadre){
						var hijos = $scope.ObjHijos(detalle,regPadre.cuenta);
						
						regPadre.hijos = hijos;
					});

					niv2.forEach(function (reg){

						var debito = reg.debito;
						var credito =reg.credito;
						
						if(reg.hijos!=null){
							reg.hijos.forEach(function (obj){
								debito += parseInt(obj.debito);
								credito += parseInt(obj.credito);
							});
						}

						var salida = {
							cuenta : reg.cuenta,
							descrip : reg.descrip,
							debito : reg.debito,
							credito: reg.credito,
						}
						cuerpo = cuerpo.concat(salida);
						
					});

					function findByMatchingProperties(set, properties) {
					    return set.filter(function (entry) {
					        return Object.keys(properties).every(function (key) {
					            return entry[key].toString().substring(0,1) === properties[key].toString()
					        });
					    });
					}

					$scope.cabeceras.forEach(function (regCab){
						var subC = findByMatchingProperties(cuerpo, {cuenta : regCab.cuenta})

						regCab.registros = subC;
						
					});

					$scope.cabeceras.sort(compare);
					}
				);
				
			}

			$scope.ObjHijos = function(hijos, padre){

				var subHijos = null;
				var nietos = null;
				var result = null;
				subHijos = hijos.filter( function (data){
					return data.padre == padre;
				});

				if(subHijos.length > 0){
					 subHijos.forEach( function (padres){
						nietos = $scope.ObjHijos(hijos, padres.cuenta)
					})
					 
					if(nietos != null){
						result=subHijos.concat(nietos);
					}else{
						result = subHijos;
					}
				}
				return result;

			}
			
		}])

		.controller('EstadoFinanController', ['$scope','$filter', 'ContabilidadService', '$window' 
					,function ($scope, $filter, ContabilidadService, $window) {
			
			$scope.fechaI = null;
			$scope.fechaF = null;
			$scope.cabeceras = [];

			$scope.getDate = function(){
				var date = new Date();
				var dateI = new Date(date.getFullYear(), date.getMonth(), 1)
				var dateF = new Date(date.getFullYear(), date.getMonth() + 1, 0);

				$scope.fechaI = $filter('date')(dateI,'dd/MM/yyyy');
				$scope.fechaF = $filter('date')(dateF,'dd/MM/yyyy');
			};

			$scope.getData = function(){
				var RegFecha = $scope.fechaI.split('/');
		      	var fechaI = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
				
				var RegFecha1 = $scope.fechaF.split('/');
		      	var fechaF = RegFecha1[2] + '-' + RegFecha1[1] + '-' + RegFecha1[0];


				ContabilidadService.getEstadoResultadoData(fechaI, fechaF).then( function (data){
					
					var cuerpo = [];

					function compare(a,b) {
					  if (a.nivel < b.nivel)
					    return -1;
					  else if (a.nivel > b.nivel)
					    return 1;
					  else 
					    return 0;
					}

					$scope.cabeceras = data.filter( function (reg){
						return reg.nivel == 1;
					});
					
					var niv2 = data.filter( function (reg){
						return (reg.tipo == 'G' && reg.nivel > 1);
					});


					var detalle = data.filter( function (reg){
						
						return reg.tipo == 'D';
					});
					
					var result = null;


					niv2.forEach(function (regPadre){
						var hijos = $scope.ObjHijos(detalle,regPadre.cuenta);
						
						regPadre.hijos = hijos;
					});

					niv2.forEach(function (reg){

						var debito = reg.debito;
						var credito =reg.credito;
						
						if(reg.hijos!=null){
							reg.hijos.forEach(function (obj){
								debito += parseInt(obj.debito);
								credito += parseInt(obj.credito);
							});
						}

						var salida = {
							cuenta : reg.cuenta,
							descrip : reg.descrip,
							debito : reg.debito,
							credito: reg.credito,
						}
						cuerpo = cuerpo.concat(salida);
						
					});

					function findByMatchingProperties(set, properties) {
					    return set.filter(function (entry) {
					        return Object.keys(properties).every(function (key) {
					            return entry[key].toString().substring(0,1) === properties[key].toString()
					        });
					    });
					}

					$scope.cabeceras.forEach(function (regCab){
						var subC = findByMatchingProperties(cuerpo, {cuenta : regCab.cuenta})

						regCab.registros = subC;
						
					});

					$scope.cabeceras.sort(compare);
					}
				);
				
			}

			$scope.ObjHijos = function(hijos, padre){

				var subHijos = null;
				var nietos = null;
				var result = null;
				subHijos = hijos.filter( function (data){
					return data.padre == padre;
				});

				if(subHijos.length > 0){
					 subHijos.forEach( function (padres){
						nietos = $scope.ObjHijos(hijos, padres.cuenta)
					})
					 
					if(nietos != null){
						result=subHijos.concat(nietos);
					}else{
						result = subHijos;
					}
				}
				return result;

			}
			
		}])

		.controller('BalanceGenCtrl', ['$scope','$filter', 'ContabilidadService', '$window' 
					,function ($scope, $filter, ContabilidadService, $window) {
			
			$scope.fechaI = null;
			$scope.fechaF = null;
			$scope.cabeceras = [];

			$scope.getDate = function(){
				var date = new Date();
				var dateI = new Date(date.getFullYear(), date.getMonth(), 1)
				var dateF = new Date(date.getFullYear(), date.getMonth() + 1, 0);

				$scope.fechaI = $filter('date')(dateI,'dd/MM/yyyy');
				$scope.fechaF = $filter('date')(dateF,'dd/MM/yyyy');
			};

			$scope.getData = function(){
				var RegFecha = $scope.fechaI.split('/');
		      	var fechaI = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
				
				var RegFecha1 = $scope.fechaF.split('/');
		      	var fechaF = RegFecha1[2] + '-' + RegFecha1[1] + '-' + RegFecha1[0];


				ContabilidadService.getEstadoResultadoData(fechaI, fechaF).then( function (data){
					
					$scope.cabeceras = data;
					
					}
				);
			}
			
		}])


		.controller('MayorController', ['$scope', '$filter', '$rootScope', 'ContabilidadService', '$timeout', '$window',
				function($scope, $filter,$rootScope, ContabilidadService, $timeout, $window){
					var date = new Date();

					$scope.dataMayor =[];
					$scope.totalCredito = 0;
					$scope.totalDebito = 0;
					$scope.SFechaI = $filter('date')(new Date(date.getFullYear(), date.getMonth(),1),'dd/MM/yyyy');
					$scope.SFechaF = $filter('date')(new Date(date.getFullYear(), date.getMonth(),28),'dd/MM/yyyy');
					$scope.panelTotal ="total-compensado"


					$scope.getMayor = function(){
						ContabilidadService.getMayorByDate($scope.SFechaI, $scope.SFechaF).then(function (data){
							$scope.dataMayor = data;
							$scope.calTotales();
						});
					};

					$scope.getMayorCuenta = function(){
						ContabilidadService.getMayorByCuenta($scope.SFechaI, $scope.SFechaF, $scope.SCuenta).then(function (data){
							$scope.dataMayor = data;
						});
					}

					$scope.PrintMayor = function($event){
						$event.preventDefault();

						$window.print();
					}

					$scope.result = function(){
						if($scope.SCuenta == undefined){
							$scope.getMayor();
						}else{
							$scope.getMayorCuenta();
						}
						$scope.calTotales();
					}

					$scope.Clear = function(){
						$scope.SFechaI = $filter('date')(new Date(date.getFullYear(), date.getMonth(),1),'dd/MM/yyyy');
						$scope.SFechaF = $filter('date')(new Date(date.getFullYear(), date.getMonth(),28),'dd/MM/yyyy');
						$scope.SCuenta = null;
						$scope.calTotales();
					};
					 
					$scope.getCuenta = function($event){
					 	$event.preventDefault();
			       
			        	$scope.tableCuentas = true;
			        	if($scope.SCuenta !== undefined) {
			                ContabilidadService.getCuentasReg().then(function (data){
			                    $scope.cuentas = data.filter(function (reg){
			                        return reg.codigo.toString().substring(0,$scope.SCuenta.length) == $scope.SCuenta;
			                    });
			                    if($scope.cuentas.length >0){
			                        $scope.tableCuentas = true;
			                        $scope.cuentaNoExiste = "";
			                    }else{
			                        $scope.tableCuentas = false;
			                        $scope.cuentaNoExiste = "No existe esta cuenta";
			                    }
			                });
			            } else {
			               ContabilidadService.getCuentasReg().then(function (data){	
			                $scope.cuentas = data;
			                $scope.cuentaNoExiste = ''; 

			              });
			            }

			        };

					$scope.calTotales = function(){
						            $scope.totalDebito = 0;
						            $scope.totalCredito = 0;
						            if($scope.dataMayor.length>0){

						                for (x = 0; x < $scope.dataMayor.length; x ++){
						                    $scope.totalDebito = $scope.totalDebito + parseFloat($scope.dataMayor[x].debito);
						                    $scope.totalCredito = $scope.totalCredito + parseFloat($scope.dataMayor[x].credito);
						                }
						                if(parseFloat($scope.totalCredito) == parseFloat($scope.totalDebito)){
						                    $scope.panelTotal ="total-compensado"
						                }else{
						                    $scope.panelTotal ="total-noCompensado"
						                }
						            }
						        };

			        $scope.selCuenta = function($event, s) {
			                $event.preventDefault();
			                $scope.SCuenta = s.codigo;
			                $scope.tableCuentas = false;
			              };

						        	
				}]);

})(_);
