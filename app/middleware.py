from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin 

class AuthMiddleware(MiddlewareMixin): 
    def process_response(self, request, response):
        '''
        認証系処理
        '''
        # トップ画面、ログイン処理画面はスルー
        if request.path == "/" or request.path.find("auth0") >= 1 or request.path == "/login_required" or request.path.find("logout") >= 1:
            return response
        
        # ログインしていない場合はログイン要求ページにリダイレクト
        if not request.user.is_authenticated: 
            return HttpResponseRedirect('/login_required') 
        
        return response
