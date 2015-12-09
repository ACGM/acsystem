(function(_){
	angular.module('cooperativa.conciliacionBanco', ['ngAnimate'])

	.factory('conciliacionServices', ['$http','$q','$filter', function ($http, $q, $filter) {
		var apiUrl='/conciliacion/banco';
		var apiUrl2='/conciliacion/banco/rg';

		function getBanco(){
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
		

		function setBanco(banco){
				var deferred = $q.defer();
			
				$http.post(apiUrl, JSON.stringify({'banco':banco}))
	                .success(function (data){
	                    deferred.resolve(data);
	                })
	                .error(function (err){
	                    deferred.resolve(err);
	                });
	            return deferred.promise;
				};

		function getBancoById(id){
			var deferred = $q.defer();

			getBanco().then(function (data){
				var result= data.filter(function (reg){
					return reg.id = id; 
				});

				if(result.length > 0){
					deferred.resolve(result);
				}else{
					deferred.reject();
				}
			});

			return deferred.response;
		};

		function getBancoByType(tipo){
			var deferred = $q.defer();

			getBanco().then(function (data){
				var result= data.filter(function (reg){
					return reg.tipo = tipo; 
				});

				if(result.length > 0){
					deferred.resolve(result);
				}else{
					deferred.reject();
				}

			});

			return deferred.response;
		}

		function getBancoFecha(fechaI, fechaF){
			var deferred = $q.defer();

			$http.get(apiUrl2+'?fechaI={fechaI}&fechaF={fechaF}'.replace('{fechaI}',fechaI).replace('{fechaF}',fechaF))
				.success(function (data){
					deferred.resolve(data);
				})
				.error(function (error){
					deferred.resolve(error);
				});

			return deferred.promise;
		};

	
		return {
			getBanco : getBanco,
			setBanco : setBanco,
			getBancoById : getBancoById,
			getBancoByType : getBancoByType,
			getBancoFecha : getBancoFecha

		};
	}])
	
	.controller('ConciliacionCtrl', ['$scope','$filter', '$rootScope', 'conciliacionServices','$timeout',  
		function ($scope, $filter, $rootScope, conciliacionServices, $timeout) {
		
		$scope.bancoLs = [];
		$scope.regBanco = {};
		$scope.fechai = null;
		$scope.fechaf = null;
		$scope.toggleBanco = false;
		$scope.NwBanco = false;
		$scope.LsBanco = true;

		$scope.getBancoList = function(){
			$scope.regBanco = {};
			conciliacionServices.getBanco().then(function (data){
				$scope.bancoLs = data;
			});
		};

		$scope.nwRegistro = function($event){
			$scope.NwBanco = true;
			$scope.LsBanco = false;
		};

		$scope.cancelarReg = function($event){
			$event.preventDefault();
			$scope.regBanco = {};
			$scope.NwBanco = false;
			$scope.LsBanco = true;
			$scope.getBancoList();
		};

		$scope.editReg = function(id){
			var reg = $scope.bancoLs.filter(function(data){
				return data.id == id;
			})
			console.log(reg[0]);
			$scope.regBanco.id = reg[0].id;
			$scope.regBanco.fecha = reg[0].fecha;

			var RegFecha = reg[0].fecha.split('-');
      		var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
      		$scope.regBanco.fecha= FechaFormat;

			$scope.regBanco.descripcion = reg[0].descripcion;
			$scope.regBanco.tipo = reg[0].tipo;
			$scope.regBanco.estatus = reg[0].estatus;
			$scope.regBanco.monto = reg[0].monto;

			$scope.nwRegistro();

		}

		$scope.getBancoFecha = function(){
			conciliacionServices.getBanco().then(function (data){
				$scope.bancoLs = data.filter(function(reg){
					var RegFecha = reg.fecha.split('-');
      				var FechaFormat = RegFecha[2] + '/' + RegFecha[1] + '/' + RegFecha[0];
      				reg.fecha = FechaFormat;

      				return reg.fecha <= $scope.fechai && reg.fecha >= $scope.fechaf; 
				});
			});
		};

		$scope.setConBanco = function($event){
			$event.preventDefault();
			try{
				debugger;
				if($scope.regBanco.id === undefined){
					$scope.regBanco.id = null;
				}

				var RegFecha = $scope.regBanco.fecha.split('/');
      			var FechaFormat = RegFecha[2] + '-' + RegFecha[1] + '-' + RegFecha[0];
      			$scope.regBanco.fecha = FechaFormat;

				console.log($scope.regBanco);
				conciliacionServices.setBanco($scope.regBanco).then(function (data){
					var resp = data;
					if (resp == "Ok"){
						notie.alert(1,"Registro almacenado de forma exitosa", 3);
					}else{
						notie.alert(3,"Ocurrio un error al realizar el registro",4);
						console.log(resp);
					}
				});
				
				$scope.cancelarReg($event);
			}
			catch(e){
				notie.alert(3,"Ocurrio un error interno en la aplicacion", 4);
				console.log(e);
			}
		};

		$scope.getBancoListType = function(tipo){
			conciliacionServices.getBancoByType(tipo).then(function (data){
				$scope.bancoLs = data;
			});
		};

		$scope.getBancoId = function(id){
			conciliacionServices.getBancoId(id).then(function (data){
				$scope.banco = data;
			});
		};

		$rootScope.mostrarError = function(error) {
			      $scope.errorMsg = error;
			      $scope.errorShow = true;
			      $timeout(function(){$scope.errorShow = false;}, 3000);   
		    };
	}]);
	
})();