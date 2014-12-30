module.exports = function(grunt){

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		uglify:{
			options:{
				banner:'/**/\n'
			},
			build: {
				src: 'acgm/static/js/*.js',
				dest: 'allApp.js'
			}
		}
	});


grunt.loadNpmTasks('grunt-contrib-uglify');

grunt.registerTask('default',['uglify']);

};