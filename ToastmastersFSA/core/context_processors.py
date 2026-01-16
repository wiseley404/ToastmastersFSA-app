from .models import SocialLink

def social_links(request):
    links = SocialLink.objects.all()
    links_dict = {link.platform: link.url for link in links}
    return {
        'social_links': links,
        'social_links_dict': links_dict
    }