using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Imagekit;

namespace RMS.services
{
    public static class ImageKitService
    {
        private static readonly ServerImagekit _imagekit = new Imagekit.Imagekit(
            SettingsService.ImageKitPublicKey,
            SettingsService.ImageKitPrivateKey,
            SettingsService.ImageKitURLEndpoint);
        
        public static async Task<string> UploadDataURI(string dataURI, string fileName)
        {
            var regexMatches = Regex.Match(dataURI, @"data:image/(?<type>.+?),(?<data>.+)");
            var type = regexMatches.Groups["type"].Value.Split(';')[0];
            
            var res = await _imagekit.FileName(fileName + "." + type).UploadAsync(dataURI);
            
            return res.FileId;
        }

        public static async Task<string> DownloadImageURL(string fileId)
        {
            var test = await _imagekit.GetFileDetailsAsync(fileId);

            return test.Url;
        }

        public static async Task DeleteImageURL(string fileId)
        {
            await _imagekit.DeleteFileAsync(fileId);
        }
    }
}