module.exports = function(grunt){

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		meta:{
				banner:'/* Archivos minificados para aplicacion de cooperativa, fecha de ultimo building <%= grunt.template.today() %> */\n'
			},
		uglify:{
			ahorro: {
				src: ['<banner>','ahorro/static/js/libs/*.js'],
				dest: 'ahorro/static/js/ahorro.js'
			}
		}
	});


grunt.loadNpmTasks('grunt-contrib-uglify');

grunt.registerTask('default',['uglify']);
//grunt.registerTask('ahorros',['ahorroMod'])

};