
(function(_){
	angular.module('cooperativa.ahorro',['ngAnimate'])

		//=================================
		//			Services  			 ==
		//=================================

		.factory('AhorroServices', ['$http','$q','$filter',function ($http, $q, $filter) {
			var apiUrl='/ahorrojson/?format=json';

			function getAllAhorro(){
				var deferred = $q.defer();

				$http.get(apiUrl+'&tipo=AR')
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
				$http.get(apiUrl+'&tipo=retiro')
					.success(function (data){
						deferred.resolve(data);
					})
					.error(function (error){
						deferred.resolve(error);
					});
				 return deferred.promise;
			}

			function setAhorroReg(AhorroSocio, maestra, cuentas, retiro){
				var deferred = $q.defer();
				$http.post(apiUrl, JSON.stringify({'AhorroSocio':AhorroSocio, 'maestra':maestra, 'cuentas':cuentas,'retiro':retiro}))
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
			$scope.idAhorro=null;
			$scope.Socio=null;
			$scope.Balance=null;
			$scope.Disponible=null;
			$scope.ArrowAhorro = "UpArrow";
			$scope.ArrowDetalle = "DownArrow";
			$scope.AhorroPanel = true;
			$scope.DetalleAhorro = false;
			$scope.MaestraDetalle=[];

			 $scope.getListaAhorro = function(){
			 	try{
					AhorroServices.getAllAhorro().then(function (data) {
						$scope.Ahorros=data;
					});
				}catch(ex){    
					
				}
			};

			$scope.toggleAhorroPanel = function(){
				$scope.AhorroPanel = !$scope.AhorroPanel;

				if($scope.AhorroPanel==true){
					$scope.ArrowAhorro = "UpArrow";
				}else{
					$scope.ArrowAhorro = "DownArrow";
				}

			}

			$scope.setAhorro = function(){
				AhorroServices.setAhorroReg($scope.DataAhorro,$scope.DataMaestra,$scope.DataCuentas,$scope.DataRetiro).then(function (data){
			 			$scope.getListaAhorro();
			 		});
			};

			$scope.AhorroById = function(Id){
				try{
                    AhorroServices.getAhorroById(Id).then(function (data){
                    	$scope.AhorrosPorSocio = data.filter(function(reg){
                    		var x =[];
                    		
                    		for(i=0; i>reg.maestra.length; i++){
                    			if(reg.maestra[i].retiro != ""){
                    				console.log(reg.maestra[i].retiro);
                    				x.push(reg);
                    			}
                    		}

                    		return x;
                    	});
                    });
                    
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



		}]); 

		

})(_);