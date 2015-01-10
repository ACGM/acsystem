(function (_){ 
	angular.module('cooperativa.Ahorro',['ngAnimate'])

    .filter('posteo', function() {
      return function (input) {
        if (!input) return "";

        input = input
                .replace('N', false)
                .replace('S', true);
        return input;
      };
    })    
	//########################
	//#		Services         # 
	//########################
	.factory('ahorroService',['$http','$q','$filter', function($http,$q,$filter){
			//================================================================
			
			function setAhorro(ahorro){
				var deferred =$q.defer();

				$http.post('http://localhost:8000/api/ahorro',JSON.stringify({'ahorro':ahorro})
					.success(function (data){
						deferred.resolve(data);
					}).error(function(data){
						deferred.resolve(data);
					})
					);
				return deferred.promises;		
			}

			//Servicio para obtener del api de ahorro de socio
			function allAhorro(){
				var deferred = $q.defer();
				$http.get('http://localhost:8000/api/ahorro')
					.success(function(data){
						deferred.resolve(data);
					});
				return deferred.promises;
			}
			//Filtro por Socio
			function ahorroBySocio(socio){
				var deferred = $q.defer();

				allAhorro().then(function (data) {
					var result= data.filter(function (AhorroSocio) {
						return AhorroSocio.socio==socio;
					});
					if( result.length > 0 ){
						deferred.resolve(result);
					}
					else{
						deferred.reject();
					}

				});
				return deferred.promises;
			}
			//Filtro por Beneficiario
			function ahorroByBeneficiario(beneficiario){
					var deferred = $q.defer();

					allAhorro().then( function (data){
						var result =data.filter(function (AhorroSocio) {
							return AhorroSocio.beneficiario== beneficiario;
						});
						if(result.length > 0){
							deferred.resolve(result);
						}else{
							deferred.reject();
						}
					});

					return deferred.promises;
			} 

			//=======================================================================	
			//Servicio para Manejo del api de Retiro de ahorros
			function allRetirosA(){
				var deferred =$q.defer();
				$http.get('api/retiroAhorro')
					.success(function (data) {
						deferred.resolve(data);
					});
					return deferred.promises;
			}

			//Filtro de retiros por socio
			function retiroBySocio(socio){
				var deferred = $q.defer();
				allRetirosA().then( function (data){
					var result= data.filter(function (RetiroAhorro){
						return RetiroAhorro.socio==socio;
					});
					if(result.length > 0){
						deferred.resolve(result);
					}
					else{
						deferred.reject();
					}

				});
				return deferred.promises;
			}
			//filtro de retiro por beneficiario
			function retiroByBeneficiario(beneficiario){
				var deferred =$q.defer();
				allRetirosA().then(function (data){
					var result= data.filter(function (RetiroAhorro){
						return retiroAhorro.beneficiario==beneficiario;
					});
					if(result.length >0 ){
						deferred.resolve(result);
					}else{
						deferred.reject();
					}
				});
				return deferred.promises;
			}
			//=======================================================================
			// Servicio para manejo del Api de la maestra de ahorro

			function allMaestraAhorro(){
				var deferred =$q.defer();
				$http.get('api/MaestraAhorro')
					.success(function (data){
						deferred.resolve(data);
					});
				return deferred.promises;

			}
			
			function maestraABySocio(socio){
				var deferred =$q.defer();
				allMaestraAhorro().then(function (data){
					var result=data.filter(function (MaestraAhorro){
						return MaestraAhorro.socio==socio;
					});
					if(result.length > 0){
						deferred.resolve(resolve);
					}else{
						deferred.reject();
					}
				});
				return deferred.promises;
			}

			function maestraAByBeneficiario(beneficiario){
				var deferred =$q.defer();
				allMaestraAhorro().then(function (data){
					var result = data.filter(function (MaestraAhorro){
						return MaestraAhorro.beneficiario==beneficiario;
					});
					if(result.length > 0){
						deferred.resolve(result);
					}else{
						deferred.reject();
					}
				});
				return deferred.promises;
			}

			return{
				allAhorro:allAhorro,
				ahorroBySocio:ahorroBySocio,
				ahorroByBeneficiario:ahorroByBeneficiario,
				allRetirosA:allRetirosA,
				retiroBySocio:retiroBySocio,
				retiroByBeneficiario:retiroByBeneficiario,
				allMaestraAhorro:allMaestraAhorro,
				maestraABySocio:maestraABySocio,
				maestraAByBeneficiario:maestraAByBeneficiario
			};
	}])
	//########################
	//		Controller       #
	//########################     
	.controller('ahorroController',['$scope','ahorroService', function($scope, ahorroService){
		$scope.errorShow= false;
		$scope.data={};
		$scope.finder='';

		$scope.findAhorro =function(){
			$scope.data=ahorroService.ahorroBySocio($scope.finder);
		};

	}
	]);
})(_);
