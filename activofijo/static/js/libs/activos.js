(function(_){
	angular.module('cooperativa.activofijo', ['ngAnimate'])

	.factory('ActivoServices', ['$http','$q','$filter',function ($http, $q, $filter) {
		var apiUrl='/activos/';
		var apiUrlD = '/depresiacion/';
		
		function getActivos(){
			var deferred = $q.defer();

			$http.get(apiUrl+'?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});
			 return deferred.promise;
		};

		function getCategoria(){
			var deferred = $q.defer();

			$http.get('/categoriaActivo/?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function	(error){
					deferred.resolve(data);
				});

			return deferred.promise;
		}

		function setActivo(regActivo){
			var deferred = $q.defer();
            $http.post(apiUrl+'?format=json', JSON.stringify({'activo':regActivo}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function setDepresiacion(fechas){
			var deferred = $q.defer();
			$http.post(apiUrlD, JSON.stringify({'fechas': fechas}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function getActivosById(id){
			var deferred = $q.defer();
			getActivos().then(function (data){
				var result = data.filter(function (reg){
					return reg.id == id;
					});

				if (result.length > 0){
					deferred.resolve(result);
				}
				else{
					deferred.reject();
				}
			});

			return deferred.promise;
		};

		function getSuplidor(){
                var deferred =$q.defer();

                $http.get('/api/suplidor/?format=json')
                .success(function (data){
                    deferred.resolve(data);})
                .error(function (err){
                    deferred.resource(err);
                });
                
                return deferred.promise;
        };

        function getLocalidad(){
        	var deferred = $q.defer();

        	$http.get('/localidades?format=json')
        		.success(function (data){
        			deferred.resolve(data);})
        		.error(function (err){
        			deferred.resolve(err);
        		});

        		return deferred.promise;

        };

        function getDocCuentas(){
			deferred = $q.defer();

			$http.get('/ahorro/?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});

				return deferred.promise;
			};

		function seeHystoric(){
			deferred = $q.defer();

			$http.get('/historicoAct?format=json')
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (err){
					deferred.resolve(err);
				});

			return deferred.promise;
		};



		return {
			getActivos 	    : getActivos,
			setActivo       : setActivo,
			getActivosById  : getActivosById,
			getSuplidor     : getSuplidor,
			setDepresiacion : setDepresiacion,
			getCategoria    : getCategoria,
			getDocCuentas	: getDocCuentas,
			getLocalidad    : getLocalidad,
			seeHystoric		: seeHystoric
		};
	}])
	
	.controller('ActivoCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout','$window', 
			function ($scope, $filter, $rootScope, ActivoServices, $timeout, $window ){

			$scope.actData = {};
			$scope.lsActivos = [];
			$scope.depList= [];
			$scope.actVs = true;
			$scope.actRg = false;
			$scope.depVs = false;
			$scope.tableSuplidor = false;
			$scope.tableCat = false;
			$scope.suplidorNombre = null;
			$scope.suplidor = null;
			$scope.categoria = null;
			$scope.CategoriaDesc = null;
			$scope.activoTmp = {};

			$scope.addAct = function($event){
				$scope.actData = null;
				$scope.actVs = false;
				$scope.actRg = true;

				$scope.actData = {};
				};


			$scope.impActivos = function($event, id){
				$event.preventDefault();
				ActivoServices.getActivosById(id).then(function (data){
					$window.sessionStorage['activo'] = JSON.stringify(data[0]);
					$window.open('/impActivo/', target='_blank'); 
				});
				};


			$scope.getCategoria = function($event){
				$event.preventDefault();
				$scope.tableCat = true;
				$scope.tableSuplidor = false;
				$scope.tableLoc = false;

				if($scope.CategoriaDesc !== null ){
					ActivoServices.getCategoria().then(function (data){
						
						$scope.categoria = data.filter(function (registro){
							return $filter('lowercase')(registro
										.descripcion.substring(0,$scope.CategoriaDesc.length)) == $filter('lowercase')($scope.CategoriaDesc);
						});

						if($scope.categoria.length > 0){
							$scope.tableCat = true;
							$scope.categoriaNoExite = '';
						}else {
							$scope.tableCat = false;
							$scope.categoriaNoExite = 'Categoria No existe';
						}
					});
					
				}
				else {
					ActivoServices.getCategoria().then(function (data){
						$scope.categoria = data;
					})
				}
				};


			$scope.selCat = function($event, s) {
                $event.preventDefault();
                $scope.CategoriaDesc = s.descripcion;
                $scope.actData.categoria = s.id;
                $scope.tableCat= false;
              };


			$scope.getSuplidor = function($event){
                $event.preventDefault();
                $scope.tableSuplidor = true;
                $scope.tableCat = false;
                $scope.tableLoc = false;
                if($scope.suplidorNombre !== null) {
                  ActivoServices.getSuplidor().then(function (data) {
                    $scope.suplidor = data.filter(function (registro) {
                       return $filter('lowercase')(registro.nombre
                                          .substring(0,$scope.suplidorNombre.length)) == $filter('lowercase')($scope.suplidorNombre);
                    });

                    if($scope.suplidor.length > 0){
                      $scope.tableSuplidor = true;
                      $scope.suplidorNoExiste = '';
                    } else {
                      $scope.tableSuplidor = false;
                      $scope.suplidorNoExiste = 'No existe el suplidor';
                    }

                  });
                } else {
                  ActivoServices.getSuplidor().then(function (data) {
                    $scope.suplidor = data;
                    $scope.suplidorCodigo = '';
                  });
                }
              };


            $scope.selSuplidor = function($event, s) {
                $event.preventDefault();
                $scope.suplidorNombre = s.nombre;
                $scope.actData.suplidor = s.id;
                $scope.tableSuplidor= false;
              };


            $scope.selLocalidad = function($event, s){
            	$event.preventDefault();
            	$scope.actData.localidad = s.id;
            	$scope.localidadD = s.Ldescripcion;
            	$scope.tableLoc = false;
            	};


            $scope.getLoc = function($event){
            	$event.preventDefault();
                $scope.tableSuplidor = false;
                $scope.tableCat = false;
                $scope.tableLoc = true;
                
                if($scope.localidadD != undefined ) {
                  ActivoServices.getLocalidad().then(function (data) {
                    $scope.localidad = data.filter(function (registro) {
                       return $filter('lowercase')(registro.descripcion
                                          .substring(0,$scope.localidadD.length)) == $filter('lowercase')($scope.localidadD);
                    });

                    if($scope.localidad.length > 0){
                      $scope.tableLoc = true;
                      $scope.suplidorNoExiste = '';
                    } else {
                      $scope.tableLoc = false;
                      $scope.suplidorNoExiste = 'Localidad no existe';
                    }

                  });
                } else {
                  ActivoServices.getLocalidad().then(function (data) {
                    $scope.localidad = data;
                    $scope.localidadCodigo = '';
                  });
                }
            	};


			$scope.lstActivos = function($event){
				ActivoServices.getActivos().then(function (data){
					$scope.lsActivos = data;

				})
				};


			$scope.guardarActivo = function($event){
				$event.preventDefault();
				if($scope.actData.id === undefined){
					$scope.actData.id = null;
				}

				var RgFechaA = $scope.actData.fechaAdq.split('/');
      			var FechaFormat = RgFechaA[2] + '-' + RgFechaA[1] + '-' + RgFechaA[0];
      			$scope.actData.fechaAdq = FechaFormat;

      			var RgFechaD = $scope.actData.fechaDep.split('/');
      			var FechaFormatD = RgFechaD[2] + '-' + RgFechaD[1] + '-' + RgFechaD[0];
      			$scope.actData.fechaDep = FechaFormatD;

				ActivoServices.setActivo($scope.actData);
				//$window.sessionStorage['activoId'] = JSON.stringify($scope.actData);
				$scope.cancelarActivo();
				$scope.lstActivos();
				//$window.open('/impActivo/', target='_blank'); 

				
            	};


            $rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   };


			$scope.volver =function($event){
				$event.preventDefault();

				$scope.actVs = true;
				$scope.actRg = false;
				$scope.depVs = false;
				}      


            $scope.getDepresiacion = function(id){
				ActivoServices.getActivosById(id).then(function (data){
					$scope.depList = data[0].depresiacion;
				});
				$scope.actVs = false;
				$scope.actRg = false;
				$scope.depVs = true;
				};


            $scope.cancelarActivo = function(){
	       		$scope.actData = null;
	       		$scope.depList = null;
	       		$scope.actVs = true;
	       		$scope.actRg = false;
	       		$scope.suplidorNombre = null;
				$scope.CategoriaDesc = null;
	       		$scope.getCategoria();
	       		};


	       	$scope.printList = function($event) {
	       		$event.preventDefault();
	       		$window.open('/historicoAct/', target='_blank'); 
	       	};

			
	}])
	
	.controller('DepresiacionCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout',
		function($scope, $filter, $rootScope, ActivoServices, $timeout){

		$scope.depList= [];
		$scope.cuentas = [];
		$scope.fechaDesp = {};
		$scope.documentos =  null;

		$rootScope.mostrarError = function(error) {
		      $scope.errorMsg = error;
		      $scope.errorShow = true;
		      $timeout(function(){$scope.errorShow = false;}, 3000);   };

		$scope.cargarData = function(){
			try{
				$scope.fechaDesp = {};
				if ($scope.documentos == null ){
					$scope.documentos = [];

					$scope.documentos = ActivoServices.getDocCuentas()
						.then(function (data){
							$scope.documentos = data.filter(function (res){
								return res.documentoId == "DEP";
									});
							console.log($scope.documentos);
					});
				}
			}
			catch(ex){
				$rootScope.mostrarError(ex.message);
			}

		};

		$scope.setDepresiacion = function (){
			try{
				
				var RgFechaA = $scope.fechaDesp.fechaI.split('/');
      			var FechaFormat = RgFechaA[2] + '-' + RgFechaA[1] + '-' + RgFechaA[0];
      			$scope.fechaDesp.fechaI = FechaFormat;

      			var RgFechaB = $scope.fechaDesp.fechaF.split('/');
      			var FechaFormat = RgFechaB[2] + '-' + RgFechaB[1] + '-' + RgFechaB[0];
      			$scope.fechaDesp.fechaF = FechaFormat;
      			console.log($scope.documentos)
				ActivoServices.setDepresiacion($scope.fechaDesp);
				
			}
			catch(ex){
				$rootScope.mostrarError(ex.message);
			}
		};
		

	}])
	
	.controller('ImpActivosCtrl', ['$scope', '$filter', '$rootScope', 'ActivoServices','$window',
		function($scope, $filter, $rootScope, ActivoServices,$window){

		$scope.Activo = JSON.parse($window.sessionStorage['activo']);
		$scope.Dep = [];
		$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

		$scope.initial = function(){
			ActivoServices.getActivosById($scope.Activo.id).then(function (data){
					var x = data[0].depresiacion;
					$scope.Dep = x;
					console.log($scope.Dep);
				});
		};
	}])

	.controller('hystoricoActivoCtrl', ['$scope', '$filter', 'ActivoServices', '$timeout',
		function($scope, $filter, ActivoServices, $timeout){
			$scope.LsData = [];
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

			$scope.initial = function(){
				ActivoServices.seeHystoric().then(function (data){
					$scope.LsData = data;
				});
				
			};
			
		}]);

})();
