namespace RMS.Extensions
{
    public static class StringExtension
    {
        /// <summary>
        /// Contains only allowed chars
        /// </summary>
        /// <param name="str">The string we want to look if it contains only the allowed chars</param>
        /// <param name="allowedChars">a string with the allowed chars</param>
        /// <returns></returns>
        public static bool ContainsOnlyAllowedChars(this string str, string allowedChars)
        {
            foreach (var c in str)
                if (!allowedChars.Contains(c))
                    return false;

            return true;
        }
        
        /// <summary>
        /// Contains only allowed chars
        /// </summary>
        /// <param name="str">The string we want to look if it contains only the allowed chars</param>
        /// <param name="allowedChars">a string with the allowed chars</param>
        /// <returns></returns>
        public static bool IsNullOrEmpty(this string str)
        {
            return string.IsNullOrEmpty(str);
        }
    }
}