
(function(_){
	angular.module('cooperativa.ahorro',['ngAnimate'])

		//=================================
		//			Services  			 ==
		//=================================

		.factory('AhorroServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/ahorrojson/';

			function getAllAhorro(){
				var deferred = $q.defer();

				$http.get(apiUrl+'?format=json&tipo=AR')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function getDocCuentas(){
				deferred = $q.defer();

				$http.get('/ahorro/?format=json')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					})

					return deferred.promise;
			}

			function getCuentaDoc(doc){
				var deferred = $q.defer();

				getCuentaDoc().then(function (data){
					var result = data.filter(function (reg){
						return reg.codigo = reg;
					});

					if(result.length > 0){
						deferred.resolve(result);
					}else{
						deferred.reject();
					}
				});

				return deferred.promise;
			}

			function getAllRetiros(){
				var deferred = $q.defer();

				$http.get(apiUrl+'?format=json&tipo=RT')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function setDiarioReg(registro){
				var deferred = $q.defer();


				$http.post('/documentoCuenta/', JSON.stringify({'registro': registro}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				return deferred.promise;
			}

			function getRetiroById(id){
				var deferred = $q.defer();
				getAllRetiros().then(function (data){
					var result = data.filter(function (reg){
						return reg.id == id;
					});

					if(result.length > 0){
						deferred.resolve(result);
					}else{
						deferred.reject();
					}
				});

				return deferred.promise;
			}

			function getAhorroById(id){
				var deferred =$q.defer();
				
				getAllAhorro().then(function (data){
					var result = data.filter(function (reg){
                        return reg.id==id;
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

			function getAhorroSocio(socio){
				var deferred = $q.defer();

				getAllAhorro().then(function (data){
					var result = data.filter(function (reg){
						return reg.socioId == socio;
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

			function getRetiroSocio(socio){
				$http.get(apiUrl+'?format=json&tipo=retiro')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function setAhorroRegS(retiro){
				var deferred = $q.defer();
				
				$http.post('/ahorro/', JSON.stringify({'retiro':retiro}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (errors){
						deferred.resolve(errors);
					});
				return deferred.promise;
			}
			
			function setIntereses(fechaI, fechaF, cuentas){
				var deferred = $q.defer();
				
				$http.post('/generarInteres/', JSON.stringify({'fechaI':fechaI, 'fechaF': fechaF}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (errors){
						deferred.resolve(errors);
					});
				return deferred.promise;
			}

			function generarAh(fecha, quincena, cuentas){
				var deferred = $q.defer();

				$http.post('/generarAhorro/', JSON.stringify({'fecha':fecha, 'quincena': quincena, 'cuentas': cuentas}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function(err){
						deferred.resolve(err);
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

			return {
				getAllAhorro : getAllAhorro,
				getRetiroSocio : getRetiroSocio,
				getAhorroSocio : getAhorroSocio,
				getAhorroById : getAhorroById,
				setAhorroRegS : setAhorroRegS,
				getAllRetiros : getAllRetiros,
				getRetiroById : getRetiroById,
				socios : socios,
				generarAh : generarAh,
				setIntereses : setIntereses,
				setDiarioReg : setDiarioReg,
				getDocCuentas : getDocCuentas
			};
		}])
		
	  	.controller('AhorroController', ['$scope', '$filter', '$window', '$rootScope', 'AhorroServices','$timeout','MaestraPrestamoService',
								function ($scope, $filter, $window , $rootScope, AhorroServices, $timeout, MaestraPrestamoService){                        	
			$scope.Ahorros=[];
			$scope.AhorrosPorSocio=[];
			$scope.AhorroHistorico=[];
			$scope.errorShow=false;
			$scope.errorMsg='';
			$scope.idAhorro=null;
			$scope.Socio=null;
			$scope.Balance=null;
			$scope.Disponible=null;
			$scope.ArrowAhorro = "UpArrow";
			$scope.ArrowDetalle = "DownArrow";
			$scope.AhorroPanel = true;
			$scope.DetalleAhorro = false;
			$scope.MaestraDetalle=[];
			$scope.tableSocio = false;
			$scope.socioReg = null;
			$scope.editer = false;
			$scope.RetiroPanel = false;
			$scope.tablePrest = false;
			$scope.documentos = null;
			$scope.retiro = {};
			$scope.cuentas = [];
			$scope.fechaI = null;
			$scope.fechaF = null;
			$scope.tempAh = [];
			$scope.flap = false;
			$scope.redId = null;
			$scope.prestamosS = {};
		    $scope.retiro['fecha'] = $filter('date')(Date.now(),'dd/MM/yyyy');

			AhorroServices.socios().then(function (data) {
				$scope.todosLosSocios = data;
			});


			$scope.limpiar = function(){
				$scope.Ahorros=[];
				$scope.AhorrosPorSocio=[];
				$scope.AhorroHistorico=[];
				$scope.errorShow=false;
				$scope.errorMsg='';
				$scope.idAhorro=null;
				$scope.Socio=null;
				$scope.Balance=null;
				$scope.Disponible=null;
				$scope.ArrowAhorro = "UpArrow";
				$scope.ArrowDetalle = "DownArrow";
				$scope.AhorroPanel = true;
				$scope.DetalleAhorro = false;
				$scope.MaestraDetalle=[];
				$scope.tableSocio = false;
				$scope.socioReg = null;
				$scope.editer = false;
				$scope.RetiroPanel = false;
				$scope.tablePrest = false;
				$scope.documentos = null;
				$scope.retiro = {};
				$scope.cuentas = [];
				$scope.fechaI = null;
				$scope.fechaF = null;
				$scope.tempAh = [];
				$scope.flap = false;
				$scope.redId = null;
				$scope.prestamosS = {};
				$scope.maestraAh =[];
			    $scope.retiro['fecha'] = $filter('date')(Date.now(),'dd/MM/yyyy');
			    $scope.numPrestamo = null;
			};


			$scope.getListaAhorro = function(){

			 	try{
					AhorroServices.getAllAhorro().then(function (data) {
						$scope.Ahorros=data;
						
						
					});

					if ($scope.documentos == null ){
						$scope.documentos = AhorroServices.getDocCuentas()
							.then(function (data){
								$scope.documentos = data.filter(function (res){
									return res.documentoId == "RAH";
								});
						});
					}
				}catch(ex){    
					$rootScope.mostrarError(ex.message);
				}
		
			};

			$scope.filterFecha = function($event){
				$event.preventDefault();
				
				if($scope.tempAh.length > 0){
					$scope.AhorrosPorSocio = $scope.tempAh;
				}else{
					$scope.tempAh = $scope.AhorrosPorSocio;
				};

				// $scope.AhorrosPorSocio 
				var RegFecha = $scope.fechaI.split('/');
  				var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
  				var fechaI = FechaFormat;

  				var RegFecha2 = $scope.fechaF.split('/');
  				var FechaFormat2 = RegFecha2[2] + '-' + RegFecha2[1] + '-' + RegFecha2[0];
  				var fechaF = FechaFormat2;
				
				var socios= $scope.maestraAh.filter(function (data) {
          			return data.fecha >= fechaI && data.fecha <= fechaF
				});
				
				$scope.maestraAh = socios;
				

			};

			$scope.printRet = function($event, retiro){
				$event.preventDefault();
				
				retiro.monto = retiro.monto * -1;

				$window.sessionStorage['retiro'] = JSON.stringify(retiro);
				$window.open('/impAhorro', target='_blank'); 

			}

			$scope.toggleAhorroPanel = function(){

				if($scope.AhorroPanel === true){
					$scope.AhorroPanel = false;
					$scope.ArrowAhorro = "DownArrow";
				}else{
					$scope.AhorroPanel = true;
					$scope.ArrowAhorro = "UpArrow";
					
				}

			}

			$scope.workflow = function($event,id){
				$event.preventDefault();
				$scope.redId = id;
				$scope.flap = true;
			};

			$scope.setAhorro = function($event){
				$event.preventDefault();
				try{
					
					if($scope.retiro.id === undefined){
						$scope.retiro.id = null;
					}

					if($scope.retiro.prestamo === undefined){
						$scope.retiro.prestamo = null;
					}


					var RegFecha = $scope.retiro.fecha.split('/');
          			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          			$scope.retiro.fecha = FechaFormat;
          			$scope.retiro.estatus = "A";
					
					AhorroServices.setAhorroRegS($scope.retiro).then(function (data){
						if(data=="Ok"){
							alert("Retiro Registrado");
						}
						return data;
					});
					
					$window.sessionStorage['retiro'] = JSON.stringify($scope.retiro);
					$window.open('/impAhorro', target='_blank'); 
					$scope.limpiar();
					$scope.getListaAhorro();

					
				}

				catch(ex){
					$rootScope.mostrarError(ex.message);
				}
				
			};

			$scope.extra = function($event,visual){
				$event.preventDefault();
				$scope.retiro.prestamo = null;
				$scope.regNumero = visual;
			};

			$scope.PostearRetiro = function($event,est){
				var reg = {};
				reg.idMaestra = $scope.redId;

				if(est == "postear"){
					reg.estatus = "P";
				}else{
					reg.estatus = "I";
				}

				$scope.redId = null;
				$scope.flap = false;

				AhorroServices.setDiarioReg(reg).then(function (data){
					if(data =="Ok"){
						alert("Registro ha sido posteado")
						$scope.getListaAhorro();
						$scope.AhorroById($scope.SocioAhorroId ,$scope.Socio);
					}
				});
			};

			$scope.AhorroById = function(Id, codigo){
				try{
					$scope.Socio = codigo
					$scope.SocioAhorroId = Id;

                    AhorroServices.getAhorroById(Id).then(function (data){
                    	
                    	$scope.AhorrosPorSocio = data.filter(function(reg){


                    		var salida = reg.maestra.filter(function(ret){
                    			return ret.retiro != '0';
                    		});
                    		return salida;
                    	});

                    	$scope.maestraAh = $scope.AhorrosPorSocio[0].maestra;
                    	
                    });
                    
                    $scope.DetalleAhorro = true;
                    $scope.toggleAhorroPanel();

                   	var xj = $scope.Ahorros.filter(function (data){
                   		return data.id==Id;
                   	});
                   	 $window.sessionStorage['ahorro'] = JSON.stringify(xj[0]);
                   	$scope.retiro['socio'] = xj[0].socioId;
                   	
					}

				catch (ex){
					$rootScope.mostrarError('Ocurrio un error al intentar cargar los datos: '+ex.message);
				}
			};

			$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		    };

	       	$scope.getSocio = function($event) {
	            $event.preventDefault();

	            $scope.tableSocio = true;
	            $scope.tableSuplidor = false;

	            if($scope.socioNombre !== undefined) {

	                $scope.socios = $scope.todosLosSocios.filter(function (registro) {
	                  return $filter('lowercase')(registro.codigo.toString()
	                                      .substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
	                 });

	                if($scope.socios.length == 0){
	                	$scope.socios = $scope.todosLosSocios.filter(function (registro) {
	                  		return $filter('lowercase')(registro.nombreCompleto
	                  			.substring(0,$scope.socioNombre.length)) == $filter('lowercase')($scope.socioNombre);
	                	});
	                }

	                if($scope.socios.length > 0){
	                  $scope.tableSocio = true;
	                  $scope.socioNoExiste = '';
	                } else {
	                  $scope.tableSocio = false;
	                  $scope.socioNoExiste = 'No existe el socio';
	                }

	            } else {
	            	$scope.socios = $scope.todosLosSocios;
	            }
	          };

            
	       	$scope.postearAHorro = function(){
	       		
	       		 $scope.showPostear = true;
	       	};

	       	$scope.selSocio = function($event, s) {
	       		$event.preventDefault();

	            $scope.socioNombre = s.codigo;

	            AhorroServices.getAllAhorro().then(function (data) {
						$scope.Ahorros=data.filter(function (reg){
							return reg.socioId == s.codigo;
						});
					});

	            $scope.tableSocio = false;
	          };

	       	$scope.newRetiro = function(){
	       		$scope.RetiroPanel = true;
	       		$scope.DetalleAhorro = false;
	       	};

	       	$scope.cancelRetiro = function(){
	       		$scope.retiro =[];
	       		$scope.RetiroPanel = false;
	       		$scope.DetalleAhorro = true	;
	       	};

	       	$scope.NoMaestra = function(){
	       		$scope.AhorroPanel=true;
	       		$scope.DetalleAhorro = false;
	       	};

	       	$scope.getRegRetiro = function(id){

	       		 AhorroServices.getAllRetiros().then(function (data){
	       		 	var result = data.filter(function (reg){
	       		 		return reg.id == id;
	       		 	});
	       		 	$scope.retiro = result[0];
	       		 });
	       		 $scope.newRetiro();
	       	};

	       	$scope.hyAhorro = function($event, socio){
	       		$event.preventDefault();
	       		
	       		var historicoSocio= $scope.Ahorros.filter(function (data){

	       			return data.socioId == socio;
	       		});

	       		$window.sessionStorage['historico'] = JSON.stringify(historicoSocio);

	       		$window.open('/impHyAhorro/', target='_blank'); 
	       	}

	       	$scope.selPrest = function($event, s){
	       		$event.preventDefault();

	       		$scope.retiro.prestamo = s.noPrestamo;
	       		$scope.numPrestamo = s.montoInicial.toString()+"-"+s.fechaAprobacion.toString(); 
	       		$scope.tablePrest = false;
	       	};


			$scope.getPrestamosSocio = function($event){
				$event.preventDefault();
				
				$scope.tablePrest = true;
	        	MaestraPrestamoService.PrestamosbySocio($scope.Socio).then(function (data){
	        		$scope.prestamosS = data.filter(function (reg){
		        			return reg.estatus != "S"
		        		});

	        		
		        	});
		        	
		    }

		}])
.controller('ImprimirAhorroController', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){        

			$scope.ahorro = JSON.parse($window.sessionStorage['ahorro']);
			$scope.retiro = JSON.parse($window.sessionStorage['retiro']);
			$scope.ahorroDt = {}
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			
			$scope.registro = function(){
				var tipo;
				var balance;
				var retiro ;
				var deuda ;
				var disponible;

				if ($scope.retiro.tipo == 'E'){
					tipo ="Retiro Ahorro";
					balance = $scope.ahorro.balance - $scope.retiro.monto;
				 	retiro = $scope.retiro.monto;
				 	deuda = ($scope.ahorro.disponible -  $scope.ahorro.balance) * -1 ;
				 	disponible = $scope.ahorro.disponible - $scope.retiro.monto;
				}
				else if($scope.retiro.tipo == 'R'){
					tipo = "Retiro por extraorinario";

					balance = $scope.ahorro.balance - $scope.retiro.monto;
				 	retiro = $scope.retiro.monto;
				 	deuda = ($scope.ahorro.disponible -  $scope.ahorro.balance) * -1 ;
				 	disponible = $scope.ahorro.disponible - $scope.retiro.monto;
				 	if(disponible < 0){
				 		disponible = 0
				 	}
				}
				

				$scope.retiro.tipo = tipo;

				$scope.ahorroDt.socioId = $scope.ahorro.socioId;
				$scope.ahorroDt.socio = $scope.ahorro.socio;
				$scope.ahorroDt.balance = balance;
				$scope.ahorroDt.disponible = disponible;
				$scope.ahorroDt.retiro = retiro;
				$scope.ahorroDt.deuda = deuda;
				


				

			}

			$scope.imprimir = function(){
				$window.print();
			};

		}])
.controller('ImpHistorico', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){

			$scope.AhorroDataRegistro = JSON.parse($window.sessionStorage['historico']);
			$scope.ahorroDt=[];
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');


			$scope.registro = function(){
				
				var RegFecha = $scope.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          		var fechaf = FechaFormat;

          		var RegFecha2 = $scope.fecha.split('/');
          		var anoInicio = parseInt(RegFecha[2])-1
          		var FechaFormat2 = anoInicio.toString() + '-' + RegFecha[1] + '-' + RegFecha[0];
          		var fechai = FechaFormat2;

          		var maestra = $scope.AhorroDataRegistro[0].maestra;
          		
				$scope.ahorroDt = maestra.filter(function (data){

					return data.fecha >= fechai && data.fecha <= fechaf && data.estatus == "P"
				})
			}


}])
.controller('GenerarAhorroCtrl', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){
			$scope.GrAhorro = [];
			$scope.quinc = [{id : 1, desc : "Quincena 1" },{id : 2, desc : "Quincena 2" }];
			$scope.documentos =  null;


			$scope.cargarData = function(){
				
					if ($scope.documentos == null ){
						$scope.documentos = AhorroServices.getDocCuentas()
							.then(function (data){
								$scope.documentos = data.filter(function (res){
									return res.documentoId == "IAH";
								});
								
						});
					}
			};

			$scope.generarAhorro = function(){
				
				var RegFecha = $scope.GrAhorro.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrAhorro.fecha = FechaFormat;


				var result = AhorroServices.generarAh($scope.GrAhorro.fecha, $scope.GrAhorro.Qui, $scope.documentos  );
			};
}])

.controller('GenerarInteresCtrl', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){
			$scope.GrInteres = [];
			$scope.documentos =  null;
			$scope.fechaI = null;
			$scope.fechaF = null;


			$scope.cargarData = function(){
				
					if ($scope.documentos == null ){
						$scope.documentos = AhorroServices.getDocCuentas()
							.then(function (data){
								$scope.documentos = data.filter(function (res){
									return res.documentoId == "RAH";
								});
								
						});
					}
			};


			$scope.generarInteres = function(){
				
				var RegFecha = $scope.fechaI.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrInteres.fechaI = FechaFormat;

          	    var RegFecha2 = $scope.fechaF.split('/');
          		var FechaFormat2 = RegFecha2[2] + '-' + RegFecha2[1] + '-' + RegFecha2[0];
          	    $scope.GrInteres.fechaF = FechaFormat2;

				var result = AhorroServices.setIntereses($scope.GrInteres.fechaI, $scope.GrInteres.fechaF).then(function (data){
					if (data == "Ok"){
						alert("Intereses generados")
					}else{
						console.log(data);
					}
				});				
			};
}]); 
})(_);