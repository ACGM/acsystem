(function(_){
	angular.module('cooperativa.reciboIng',['ngAnimate'])

		.factory('reciboIngServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/reciboIngreso';

			function getRecibos(){
				var deferred = $q.defer();

				$http.get(apiUrl+"?format=json")
					.success(function (data) {
						deferred.resolve(data);
					})
					.error(function (err){
						deferred.resolve(err);
					})

					return deferred.promise;
			};

			function getReciboBySocio(socio){
				var deferred = $q.defer();

				getRecibos.then(function (data){
					var registro = data.filter(function (reg){
						return reg.socio == socio;
					});

					deferred.resolve(registro);
				});

				return deferred.promise;
			};

			function setRecibo(recibo){
				var deferred = $q.defer();

				$http.post(apiUrl, JSON.stringify({'recibo': recibo}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (err){
						 deferred.resolve(err);
					});

				return deferred.promise;
			};

			function socios() {
                var deferred = $q.defer();

                $http.get('/api/socio/?format=json')
                  .success(function (data) {
                    deferred.resolve(data.filter( function(socio) {
                      return socio.estatus == "E" || socio.estatus == "S";

                    }));
                  });
                  return deferred.promise;
            };

            function postRecibo(recibo, fecha){
            	var deferred = $q.defer();
            	$http.post('/postearRecibo', JSON.stringify({'recibo': recibo,'fecha': fecha}))
            		.success(function (data){
            			deferred.resolve(data);
            		})
            		.error(function (err){
            			deferred.resolve(err);
            		});

            	return deferred.promise;
            }

			return {
				getRecibos : getRecibos,
				getReciboBySocio : getReciboBySocio,
				setRecibo : setRecibo,
				socios : socios,
				postRecibo : postRecibo
			};
		}])
		
	  	.controller('reciboIngCtrl', ['$scope', '$filter', '$window', '$rootScope', 'reciboIngServices','$timeout', '$window', 'MaestraPrestamoService',
								function ($scope, $filter, $window , $rootScope, reciboIngServices, $timeout, $window, MaestraPrestamoService){                        	
			
			$scope.reciboData = {}
			$scope.reciboLista = [];
			$scope.prestamosS = [];
			$scope.reciboLst = true;
			$scope.reciboCr = false;
			$scope.tableSocio = false;
			$scope.tablePrest =  false;
			$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');

		    //Traer todos los socios a javascript
	        reciboIngServices.socios().then(function (data) {
	          $scope.todosLosSocios = data;
	        });

	        $scope.cancelarReg = function($event){
	        	$scope.reciboData = {}
				$scope.reciboLista = [];
				$scope.prestamosS = [];
				$scope.reciboLst = true;
				$scope.reciboCr = false;
				$scope.tableSocio = false;
				$scope.tablePrest =  false;
				$scope.fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
	        }

			$scope.getList = function(){

				$scope.reciboLista =[];

				reciboIngServices.getRecibos().then(function (data) {
					$scope.reciboLista = data;
					console.log(data);
				});
			}



			$scope.nwRecibo = function($event){
				$scope.reciboLst = false;
				$scope.reciboCr = true;
			}

			$scope.editRecibo = function($event, id){
				$event.preventDefault();

				$scope.reciboLista.filter(function (data){
					var reg = data.filter(function (registro){
						return registro.id == id;
					});
					$scope.reciboData.id = reg[0].id;
					$scope.reciboData.fecha = reg[0].fecha;
					$scope.reciboData.socio =reg[0].socioId;
					$scope.socioNombre = reg[0].socio;
					$scope.reciboData.montoAhorro = reg[0].montoAhorro;
					$scope.reciboData.NoPrestamo = reg[0].prestamo.codigo;
					$scope.montoInicial = reg[0].prestamo.montoInicial;
					$scope.reciboIngreso.montoPrestamo =reg[0].montoPrestamo;

				});
			}

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
	                $scope.socioCodigo = '';
	            }
	          };

	        $scope.selPrest = function($event, x){
	       		$event.preventDefault();

	       		$scope.reciboData.NoPrestamo=x.noPrestamo;
	            $scope.montoInicial = x.montoInicial;

	            $scope.tablePrest = false;
	          };

	       	$scope.selSocio = function($event, s) {
	       		$event.preventDefault();

	       		$scope.reciboData.socio=s.codigo;
	            $scope.socioNombre = s.nombreCompleto;

	            $scope.tableSocio = false;
	          };

	        $scope.getPrestamosSocio = function($event){

	        	MaestraPrestamoService.PrestamosbySocio($scope.reciboData.socio).then(function (data){
	        		$scope.prestamosS = data.filter(function (reg){
	        			console.log(reg);
		        			return reg.estatus != "S"
		        		});
		        	});
		        	$scope.tablePrest = true;
		        	}

	        $rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		    	};

		    $scope.postRecibo = function($event,id){
		    	$event.preventDefault();

		    	var fecha = $filter('date')(Date.now(),'dd/MM/yyyy');
		    	var RegFecha = $scope.fecha.split('/');
          		var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          		fecha = FechaFormat;
		    	reciboIngServices.postRecibo(id, fecha).then(function (data){
		    		if(data == "Ok"){
		    			alert("Recibo #"+id+" ha sido Posteado")
		    			$scope.reciboLst = true;
						$scope.reciboCr = false;
						$scope.tableSocio = false;
						$scope.tablePrest =  false;
		    			$scope.getList();
		    		}else{
		    			$rootScope.mostrarError("Ha Ocurrido un error al intentar postear el recibo #"+id)
		    		}
		    	});
		    };

	        $scope.setRecibo = function($event){
	        	$event.preventDefault();
	  	        	var RegFecha = $scope.fecha.split('/');
          			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
          			$scope.reciboData.fecha = FechaFormat;

          			if ($scope.reciboData.id == undefined){
          				$scope.reciboData.id = null;
          			}

          			if ($scope.reciboData.estatus == undefined){
          				$scope.reciboData.estatus = "R";
          			}

          		try{
          			reciboIngServices.setRecibo($scope.reciboData).then(function (data){
          				console.log(data);
          			});
          			 $scope.cancelarReg($event);
          			 $scope.getList();
          		}	
          		catch(ex){
          			$rootScope.mostrarError(ex.message);
          		}
	        	};

}]); 
})(_);