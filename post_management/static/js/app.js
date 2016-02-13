var app = angular.module('clientApp', ['ngRoute',])

app.config(['$routeProvider', function($routeProvider){
	$routeProvider
		.when('/', {
			controller: 'indexController',
			templateUrl: '/feedpost_management/static/partial/blog_feed.html'
		})
		.when('/topic/:id', {
			controller: 'postController',
			templateUrl: '/feedpost_management/static/partial/post.html'
		})
}])

app.service('social', ['$window', '$q', '$http', function($window, $q, $http) {
	var promise = null;
	var data = null;
	var retries = 0
	$window.resolve = function(_data) {
		data = _data;
		promise.resolve();
	}
	var comment = function (text, id) {
		$http({
			method:'POST',
			url: '/social/comment/'+id,
			data: {'comment_text': text}
		}).success(function(data, status) {
			console.log(data)
			retries = 0;
		}).error(function(data, status) {
			if(status == 401 && retries<3)
				openWindow(function(data) {
					retries+=1;
					comment(text, id)
				})
		})
	}
	var openWindow = function(callback) {
		promise = $q.defer();
		var v = $window.open('https://www.facebook.com/dialog/oauth?client_id=1653101508290097&redirect_uri=http://localhost:5000/social/auth/fb','','scrollbars=1')
		
		$q.when(promise).then(function() {
			callback(data)
		})
	}
	return {
		comment: comment,
		openWindow: openWindow
	}
}])

app.controller('indexController', ['$http', '$scope','$location',  function($http, $scope, $location) {
	$scope.getPosts = function() {
		$http({
			url: '/feed/api/post',
			method: 'GET'
		}).success(function(data) {

			$scope.posts = data.data;
		})
	}
	$scope.redirect = function(id) {
		$(document).scrollTop(0)
		$location.url('topic/'+id)

	}
	$scope.getPosts();
}])

app.controller('postController', ['$http', '$scope', '$routeParams','social', function($http,$scope, $routeParams, social) {
	$scope.getPost = function() {
		var id = $routeParams.id;

		$http({
			url: '/feed/api/post/'+id,
			method: 'GET'
		}).success(function(data) {
			$('.article-text').append(markdown.toHTML(data.data.text))
			$scope.id = id
			$scope.post = data.data;
		})
	}
	$scope.comment = function() {

		social.comment($scope.comment_text, $scope.id);
	}

	$scope.getPost();
}])