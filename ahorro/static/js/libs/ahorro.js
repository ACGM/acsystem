
(function(_){
	angular.module('cooperativa.ahorro',['ngAnimate'])

		//=================================
		//			Services  			 ==
		//=================================

		.factory('AhorroServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/ahorrojson/?format=json';

			function getAllAhorro(){
				var deferred = $q.defer();
				
				$http.get(apiUrl)
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
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
						return reg.socio == socio;
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
				$http.get(apiUrl+'&tipo=retiro')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function setAhorroReg(ahorroSocio){
				var deferred = $q.defer();
				$http.post("/ahorrojson/&Ref=Ahorrro&Ret=Ah", JSON.stringify({'AhorroSocio':ahorroSocio}))
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (errors){
						deferred.resolve(errors);
					});
				return deferred.promise;
			}

			
		
			return {
				getAllAhorro: getAllAhorro,
				getRetiroSocio: getRetiroSocio,
				getAhorroSocio: getAhorroSocio,
				getAhorroById: getAhorroById,
				setAhorroReg: setAhorroReg
				
			};
		}])
		
		.controller('AhorroController', ['$scope', '$filter', '$rootScope', 'AhorroServices','$timeout',
								function ($scope, $filter, $rootScope, AhorroServices, $timeout){
			
			$scope.Ahorros=[];
			$scope.AhorrosPorSocio=[];
			$scope.AhorroHistorico=[];
			$scope.errorShow=false;
			$scope.errorMsg='';
			$scope.Socio='';
			$scope.TemplateData=[{
							'id':null,
							'socio':'2',
							'balance':'35000',
							'disponible':'35000',
							'maestra':[{
								'id':null,
								'fecha':'01/01/2015',
								'monto':'35000',
								'interes':'1',
								'balance':'35000',
								'estatus':false,
								'cuentas': [{
									'fecha':'01/01/2015',
									'cuenta': '1',
									'referencia':'Ar',
									'tipoDoc' : '1',
									'estatus' : false,
									'debito' : '35000',
									'credito' : '0.00'
								},
								{
									'fecha':'01/01/2015',
									'cuenta': '2',
									'referencia':'Ar',
									'tipoDoc' : '1',
									'estatus' : false,
									'debito' : '0.00',
									'credito' : '35000'
								}]
							}]
			}];

			 $scope.getListaAhorro = function(){
			 	try{
					AhorroServices.getAllAhorro().then(function (data) {
						$scope.AhorrosPorSocio=data;
					});
				}catch(ex){
					$rootScope.mostrarError(ex.message);
				}
			};

			$scope.setAhorro = function(){
				AhorroServices.setAhorroReg($scope.TemplateData).then(function (data){
			 			console.log(data);
			 		});
			};

			$scope.AhorroById = function(id){
			//	try{
					AhorroServices.getAhorroById(id).then(function (data){
						$scope.Ahorros=data;
						console.log(data);
					});
				// }
				// catch (ex){
				// 	$rootScope.mostrarError(ex.message);
				// }
			}; 
			//  $scope.getHistoricoAhorro = function(){
			// 	AhorroServices.getAhorroSocio($scope.Socio).then(function (data){
			// 		$scope.AhorroHistorico=data;
			// 	});
			// };

			  $rootScope.mostrarError = function(error) {
		        $scope.errorMsg = error;
		        $scope.errorShow = true;
		         $timeout(function(){$scope.errorShow = false;}, 3000);   

		      };



		}]); 

		

})(_);