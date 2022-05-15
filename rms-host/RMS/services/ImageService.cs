using System;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.Extensions.Caching.Memory;
using RMS.services.Interfaces;

namespace RMS.services
{
    public class ImageService : IImageService
    {
        private static MemoryCache _cache = new MemoryCache(new MemoryCacheOptions());

        public async Task<string> UploadDataURI(string dataURI, string fileName)
        {
            return await ImageKitService.UploadDataURI(dataURI, fileName);
        }

        public async Task<string> DownloadImageURL(string fileId)
        {
            // Try to retrieve image URL from cache
            if (!_cache.TryGetValue($"ImageKit{fileId}", out string imageUrl))
            {
                // Image not in cache, so retrieve it from image kit
                imageUrl = await ImageKitService.DownloadImageURL(fileId);
                
                // Make sure it gets cleared after a day of not being accessed
                // and the priority is set to normal so it can be deleted
                var cacheOptions = new MemoryCacheEntryOptions()
                    .SetSlidingExpiration(TimeSpan.FromDays(1))
                    .SetPriority(CacheItemPriority.Normal);
                
                // Insert the image in the cache
                _cache.Set($"ImageKit{fileId}", imageUrl, cacheOptions);
            }
            
            return imageUrl;
        }

        public async Task DeleteImageURL(string fileId)
        {
            if (_cache.TryGetValue($"ImageKit{fileId}", out string imageUrl))
            {
                _cache.Remove($"ImageKit{fileId}");
            }
            
            await ImageKitService.DeleteImageURL(fileId);
        }
    }
}