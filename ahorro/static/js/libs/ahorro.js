
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

			function getCuentaDocDoc(doc){
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

			function setDiarioReg(cuenta){
				var deferred = $q.defer();

				$http.post('/contabilidad/RegDiario/', JSON.stringify({'cuenta': cuenta}))
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

			function setAhorroRegS(retiro, cuenta){
				var deferred = $q.defer();
				
				$http.post('/ahorro/', JSON.stringify({'retiro':retiro,'cuenta': cuenta}))
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
				
				$http.post('/generarInteres/', JSON.stringify({'fechaI':fechaI, 'fechaF': fechaF,'cuentas': cuentas}))
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
		
	  	.controller('AhorroController', ['$scope', '$filter', '$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter, $window , $rootScope, AhorroServices, $timeout){                        	
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
			$scope.documentos = null;
			$scope.retiro = {};
			$scope.cuentas = [];
		    $scope.retiro['fecha'] = $filter('date')(Date.now(),'dd/MM/yyyy');

			AhorroServices.socios().then(function (data) {
				$scope.todosLosSocios = data;
			});

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

			$scope.toggleAhorroPanel = function(){

				if($scope.AhorroPanel === true){
					$scope.AhorroPanel = false;
					$scope.ArrowAhorro = "DownArrow";
				}else{
					$scope.AhorroPanel = true;
					$scope.ArrowAhorro = "UpArrow";
					
				}

			}

			$scope.setAhorro = function($event){
				$event.preventDefault();
				try{
					if($scope.retiro.id === undefined){
						$scope.retiro.id = null;
					}
					var RegFecha = $scope.retiro.fecha.split('/');
          			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          			$scope.retiro.fecha = FechaFormat;
					
					AhorroServices.setAhorroRegS($scope.retiro, 0).then(function (data){
						$scope.retiro.id = data
						return data;
					});

					window.setTimeout($scope.setCuentas(),4000);
					
					$window.sessionStorage['retiro'] = JSON.stringify($scope.retiro);

					$scope.getListaAhorro();

					// $scope.cancelRetiro();
					// $scope.NoMaestra();
					//$window.open('/impAhorro/', target='_blank'); 
				}

				catch(ex){
					$rootScope.mostrarError(ex.message);
				}
				
			};

			$scope.setCuentas = function(){
				for (var x=0; x < $scope.documentos.length; x++) {
					
					var cuenta = {}
						cuenta.codCuenta = $scope.documentos[x].cuenta;
						if($scope.documentos[x].accion == "D"){
							cuenta.debito = $scope.retiro.monto;
							cuenta.credito = 0;	
						}else{
							cuenta.debito = 0;
							cuenta.credito = $scope.retiro.monto;
						}
						cuenta.fecha = $scope.retiro.fecha;
						cuenta.ref = "RAH-" + $scope.retiro.socio.toString();
						cuenta.estatus = "A"

					AhorroServices.setDiarioReg(cuenta).then(function (data){
						var salida = AhorroServices.setAhorroRegS($scope.retiro, data);
						return data;
					});
					
					}
				
			}

			$scope.AhorroById = function(Id){
				try{

                    AhorroServices.getAhorroById(Id).then(function (data){
                    	
                    	$scope.AhorrosPorSocio = data.filter(function(reg){


                    		var salida = reg.maestra.filter(function(ret){
                    			return ret.retiro != '0';
                    		});
                    		return salida;
                    	});
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

		}])
.controller('ImprimirAhorroController', ['$scope', '$filter','$window', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter,$window, $rootScope, AhorroServices, $timeout){        

			$scope.ahorro = JSON.parse($window.sessionStorage['ahorro']);
			$scope.retiro = JSON.parse($window.sessionStorage['retiro']);
			$scope.ahorroDt = {}
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			
			$scope.registro = function(){
				var balance = $scope.ahorro.balance - $scope.retiro.monto;
				var retiro = $scope.retiro.monto;
				var deuda = $scope.ahorro.balance - $scope.ahorro.disponible;
				var libre = (disponible - deuda)- retiro;


				var disponible = $scope.ahorro.disponible - $scope.retiro.monto;

				$scope.ahorroDt.socioId = $scope.ahorro.socioId;
				$scope.ahorroDt.socio = $scope.ahorro.socio;
				$scope.ahorroDt.balance = balance;
				$scope.ahorroDt.disponible = disponible;
				$scope.ahorroDt.retiro = retiro;
				$scope.ahorroDt.deuda = deuda;
				$scope.ahorroDt.libre = libre;



				var tipo;

				if ($scope.retiro.tipo == 'A'){
					tipo ="Retito de Ahorro";
				}
				else if($scope.retiro.tipo == 'J'){
					tipo = "Retiro por Ajuste";
				}
				else{
					tipo = "Retiro Otros";
				}

				$scope.retiro.tipo = tipo;

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
          		
				$scope.ahorroDT = maestra.filter(function (data){
					return data.fecha >= fechai && data.fecha <= fechaf
				});		
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
								console.log($scope.documentos);
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


			$scope.cargarData = function(){
				
					if ($scope.documentos == null ){
						$scope.documentos = AhorroServices.getDocCuentas()
							.then(function (data){
								$scope.documentos = data.filter(function (res){
									return res.documentoId == "RAH";
								});
								console.log($scope.documentos);
						});
					}
			};


			$scope.generarInteres = function(){

				var RegFecha = $scope.GrInteres.fechaI.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrInteres.fechaI = FechaFormat;

          	    var RegFecha2 = $scope.GrInteres.fechaF.split('/');
          		var FechaFormat2 = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          	    $scope.GrInteres.fechaF = FechaFormat2;

          	    $scope.cuenta = getAhorroSocio.getCuentaDoc('IAH');

				var result = AhorroServices.setIntereses($scope.GrInteres.fechaI, $scope.GrInteres.fechaF, $scope.documentos);				
			};
}]); 
})(_);