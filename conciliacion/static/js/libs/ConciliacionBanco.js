(function(_){
	angular.module('cooperativa.conciliacionBanco', ['ngAnimate'])

	.factory('conciliacionServices', ['$http','$q','$filter', function ($http, $q, $filter) {
		var apiUrl='/conciliacion/banco/';
		var apiUrl2='/conciliacion/banco/rg/';

		function getBanco(){
			var defered = $q.defer();

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

				http.post(apiUrl, JSON.stringify({'Notas':notas}))
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
		$scope.banco = null;
		$scope.toggleBanco = false;

		$scope.getBancoList = function(){
			conciliacionServices.getBanco().then(function (data){
				$scope.bancoLs = data;
			});
		};

		$scope.setConBanco = function($event){
				try{
					conciliacionServices.setBanco($scope.banco).then(function (data){
						var resp = data;
					});
				}
				catch(e){
					$rootScope.mostrarError(e);
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
	}]);
	
})();