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

            $http.post(apiUrl, JSON.stringify({'activo':regActivo}))
                .success(function (data){
                    deferred.resolve(data);
                })
                .error(function (err){
                    deferred.resolve(err);
                });
            return deferred.promise;
		};

		function setDepresiacion(cuentas, fechaF){
			var deferred = $q.defer();

			$http.post(apiUrlD, JSON.stringify({'cuentas':cuentas,'fechaF': fechaF}))
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

			getActivos.then(function (data){
				var result = data.filter(function (reg){
					return reg.id = id;
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

		return {
			getActivos 	    : getActivos,
			setActivo       : setActivo,
			getActivosById  : getActivosById,
			getSuplidor     : getSuplidor,
			setDepresiacion : setDepresiacion,
			getCategoria    : getCategoria
		};
	}])
	
	.controller('ActivoCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout', 
			function ($scope, $filter, $rootScope, ActivoServices, $timeout ){

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

			$scope.addAct = function($event){
				$scope.actData = null;
				$scope.actVs = false;
				$scope.actRg = true;

			};

			$scope.getCategoria = function($event){
				$event.preventDefault();
				$scope.tableCat = true;

				if($scope.CategoriaDesc !== undefined ){
					ActivoServices.getCategoria().then(function (data){
						$scope.categoria = data.filter(function (registro){
							return $filter('lowercase')(registro.descripcion
														.substring(0,$scope.CategoriaDesc.length)) == $filter('lowercase')($scope.CategoriaDesc);
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
			
			}

			 $scope.selCat = function($event, s) {
                $event.preventDefault();
                $scope.CategoriaDesc = s.descripcion;
                $scope.actData.categoria = s.id;
                console.log($scope.actData);
                $scope.tableSuplidor= false;
              };

			$scope.getSuplidor = function($event){
                    $event.preventDefault();
                    $scope.tableSuplidor = true;
                    if($scope.suplidorNombre !== undefined) {
                      ActivoServices.getSuplidor().then(function (data) {
                        $scope.suplidor = data.filter(function (registro) {
                           return $filter('lowercase')(registro.nombre
                                              .substring(0,$scope.suplidorNombre.length)) == $filter('lowercase')($scope.suplidorNombre);
                        });
                        console.log(data);

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
                console.log($scope.actData);
                $scope.tableSuplidor= false;
              };


			$scope.lstActivos = function($event){
				ActivoServices.getActivos().then(function (data){
					$scope.lsActivos = data;
				})
			};

			$scope.guardarActivo = function($event){
				$event.preventDefault();
				try{
					if($scope.actData.id === undefined){
						$scope.actData.id = null;
					}

					var RgFechaA = $scope.actData.fechaAdq.split('/');
          			var FechaFormat = RgFechaA[2] + '-' + RgFechaA[1] + '-' + RgFechaA[0];
          			$scope.fechaAdq.fechaAdq = FechaFormat;

          			var RgFechaD = $scope.actData.fechaAdq.split('/');
          			var FechaFormatD = RgFechaD[2] + '-' + RgFechaD[1] + '-' + RgFechaD[0];
          			$scope.fechaAdq.fechaDep = FechaFormatD;

					var result = ActivoServices.setActivo($scope.actData);
					//$window.sessionStorage['activoId'] = JSON.stringify($scope.actData);
					$scope.lstActivos();
					$scope.cancelarActivo();
					//$window.open('/impActivo/', target='_blank'); 

				}
				catch(ex){
					$rootScope.mostrarError(ex.message);
				}
            };

            $scope.getDepresiacion = function(id){
				ActivoServices.getActivosById(id).then(function (data){
					$scope.depList = data.depresiacion;
				});
			};

            $scope.cancelarActivo = function(){
	       		$scope.actData = null;
	       		$scope.depList = null;
	       		$scope.actVs = true;
	       		$scope.actRg = false;
	       	};

			
	}])
	
	.controller('DepresiacionCtrl', ['$scope','$filter', '$rootScope', 'ActivoServices','$timeout',
		function($scope, $filter, $rootScope, $ActivoServices, $timeout){

			$scope.depList= [];
			$scope.cuentas = [];
			$scope.fechaDesp = null;

			$scope.setDepresiacion = function (){
				try{
					if ($scope.cuentas.length > 0){
						ActivoServices.setDepresiacion($scope.cuentas, $scope.fechaDesp);
					}
					else{
						$rootScope.mostrarError("No hay cuentas definidas.");
					}

				}
				catch(ex){
					$rootScope.mostrarError(ex.message);
				}

				
			};
			

		}]);

})();
