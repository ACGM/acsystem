
(function(_){
	angular.module('cooperativa.ahorro',['ngAnimate'])

		//=================================
		//			Services  			 ==
		//=================================

		.factory('AhorroServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			
			function getAllAhorro(){
				var deferred = $q.defer();
				var apiUrl='/ahorrojson/?format=json';

				$http.get(apiUrl)
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
			}

			function getAhorroSocio(socio){
				var deferred = $q.defer();

				getAllAhorro().then(function (data){
					var result = data.filter(function (reg){
						return reg.socio == socio;
					});
					
					if(result.length > 0){
						deferred.resolve(result);
					}
					else{
						deferred.reject();
					}
				});
			}

			function getRetiroSocio(socio){
				$http.get(apiUrl+'&tipo=retiro')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					})
			}


			
		
			return {
				getAllAhorro: getAllAhorro,
				getRetiroSocio: getRetiroSocio,
				getAhorroSocio: getAhorroSocio
				
			};
		}])
		
		.controller('AhorroController', ['$scope', '$filter', '$rootScope', 'AhorroServices',
								function ($scope, $filter, $rootScope, AhorroServices){
			
			$scope.AhorrosPorSocio=[];
			$scope.AhorroHistorico=[];
			$scope.errorShow=false;
			$scope.errorMsg='';
			$scope.Socio='242126';

			 $scope.getCabecera = function(){
			 	try{
					AhorroServices.getAllAhorro().then(function (data) {
						$scope.AhorrosPorSocio=data;
						console.log(data);
					});
				}catch(ex){
					debugger;
					$rootScope.mostrarError(ex.message);
				}
			}

			 $scope.getHistoricoAhorro = function(){
				AhorroServices.getAhorroSocio($scope.Socio).then(function (data){
					$scope.AhorroHistorico=data;
				});
			}

			  $rootScope.mostrarError = function(error) {
		        $scope.errorMsg = error;
		        $scope.errorShow = true;
		        console.log('test agregado para que suba a git');
		      }

		}]) 

		

})(_);