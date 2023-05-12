using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Xml.Linq;
using CsvHelper;
using CsvHelper.Configuration;

namespace battery_csv_bytes_conversion
{

    public class read_help_pk_navi // for reading the "help .csv files" for BQ4050 and BQ78350
    {
        public string CLASS { get; set; }
        public string SUBCLASS { get; set; }
        public string NAME { get; set; }
        public string ADDRESS { get; set; }
        public string OFFSET { get; set; }
        public string NUM_READS { get; set; }
        public string TYPE { get; set; }
        public string UNIT { get; set; }
        public string MeasuredValue { get; set; }  // Add this line
    }

    public class byte_data_pk_navi // for reading the "raw data byte .csv files" for BQ4050 and BQ78350
    {
        [CsvHelper.Configuration.Attributes.Index(0)]
        public string ADDRESS { get; set; }
        [CsvHelper.Configuration.Attributes.Index(1)]
        public string DATA { get; set; }
    }

    public class read_help_rheo // for reading the "help .csv files" for BQ3060
    {
        public string CLASS { get; set; }
        public string SUBCLASS { get; set; }
        public string NAME { get; set; }
        public string SUBCLASS_ID { get; set; }
        public string OFFSET { get; set; }
        public string NUM_READS { get; set; }
        public string TYPE { get; set; }
        public string UNIT { get; set; }
        public string MeasuredValue { get; set; }  // Add this line
    }

    public class byte_data_rheo // for reading the "raw data byte .csv files" for BQ3060
    {
        [CsvHelper.Configuration.Attributes.Index(0)]
        public string SUBCLASS_ID { get; set; }
        [CsvHelper.Configuration.Attributes.Index(1)]
        public string DATA { get; set; }
    }

    internal class Program
    {

        public static int HexStringToInt(string hexString)
        {
            if (hexString.StartsWith("0x"))
            {
                // Remove "0x" prefix from hexadecimal string
                hexString = hexString.Substring(2);
                return Convert.ToInt32(hexString, 16);
            }
            else
            {
                // Remove spaces from hexadecimal string
                hexString = hexString.Replace(" ", "");
                return Convert.ToInt32(hexString, 16);
            }
        }

        public static string ConvertEndianess(string input)
        {
            // Split the string into an array of strings (bytes) using space as delimiter
            string[] bytes = input.Split(' ');

            // Reverse the order of the bytes
            string[] reversedBytes = bytes.Reverse().ToArray();

            // Concatenate the reversed bytes back into a single string with spaces in between
            string output = string.Join(" ", reversedBytes);

            return output;
        }

        public static uint ConvertToUnsignedInt(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
            {
                throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));
            }

            // Remove all whitespace characters from the input
            input = input.Replace(" ", string.Empty);

            // Check that the input length is a multiple of 2
            if (input.Length % 2 != 0)
            {
                throw new ArgumentException("Input must contain only two-digit hexadecimal numbers.", nameof(input));
            }

            // Split the input into two-digit hexadecimal numbers
            string[] bytesAsStrings = Enumerable.Range(0, input.Length / 2).Select(i => input.Substring(i * 2, 2)).ToArray();

            byte[] bytes;
            try
            {
                bytes = bytesAsStrings.Select(s => Convert.ToByte(s, 16)).Reverse().ToArray();
            }
            catch (Exception ex)
            {
                throw new ArgumentException("Error converting input to bytes. Make sure the input contains only valid hexadecimal numbers.", nameof(input), ex);
            }

            uint output = 0;

            if (bytes.Length == 1)
            {
                output = bytes[0];
            }
            else if (bytes.Length == 2)
            {
                output = BitConverter.ToUInt16(bytes, 0);
            }
            else if (bytes.Length == 4)
            {
                output = BitConverter.ToUInt32(bytes, 0);
            }
            else
            {
                throw new ArgumentException("Input must contain 1, 2, or 4 bytes.");
            }

            return output;
        }

        public static int ConvertToSignedInt(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
            {
                throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));
            }

            // Remove all whitespace characters from the input
            input = input.Replace(" ", string.Empty);

            // Check that the input length is a multiple of 2
            if (input.Length % 2 != 0)
            {
                throw new ArgumentException("Input must contain only two-digit hexadecimal numbers.", nameof(input));
            }

            // Split the input into two-digit hexadecimal numbers
            string[] bytesAsStrings = Enumerable.Range(0, input.Length / 2).Select(i => input.Substring(i * 2, 2)).ToArray();

            byte[] bytes;
            try
            {
                bytes = bytesAsStrings.Select(s => Convert.ToByte(s, 16)).Reverse().ToArray();
            }
            catch (Exception ex)
            {
                throw new ArgumentException("Error converting input to bytes. Make sure the input contains only valid hexadecimal numbers.", nameof(input), ex);
            }

            int output = 0;

            if (bytes.Length == 1)
            {
                output = (sbyte)bytes[0];
            }
            else if (bytes.Length == 2)
            {
                output = BitConverter.ToInt16(bytes, 0);
            }
            else if (bytes.Length == 4)
            {
                output = BitConverter.ToInt32(bytes, 0);
            }
            else
            {
                throw new ArgumentException("Input must contain 1, 2, or 4 bytes.");
            }

            return output;
        }

        public static string ConvertToAscii(string input)
        {
            if (string.IsNullOrWhiteSpace(input))
            {
                throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));
            }

            // Remove all whitespace characters from the input
            input = input.Replace(" ", string.Empty);

            // Check that the input length is a multiple of 2
            if (input.Length % 2 != 0)
            {
                throw new ArgumentException("Input must contain only two-digit hexadecimal numbers.", nameof(input));
            }

            // Split the input into two-digit hexadecimal numbers
            string[] bytesAsStrings = Enumerable.Range(0, input.Length / 2).Select(i => input.Substring(i * 2, 2)).ToArray();

            byte[] bytes;
            try
            {
                bytes = bytesAsStrings.Select(s => Convert.ToByte(s, 16)).ToArray();
            }
            catch (Exception ex)
            {
                throw new ArgumentException("Error converting input to bytes. Make sure the input contains only valid hexadecimal numbers.", nameof(input), ex);
            }

            // Convert the byte array to an ASCII string
            string output = Encoding.ASCII.GetString(bytes);

            return output;
        }

        static float BQ4050_HexStringToFloat(string hexString)
        {
            hexString = hexString.Replace(" ", "");
            uint num = uint.Parse(hexString, System.Globalization.NumberStyles.AllowHexSpecifier);

            byte[] floatVals = BitConverter.GetBytes(num);
            float f = BitConverter.ToSingle(floatVals, 0);
            return f;
        }
        static float BQ78350_HexStringToFloat(string hexString, string name_of_float)
        {
            hexString = hexString.Replace(" ", "");
            uint num = uint.Parse(hexString, System.Globalization.NumberStyles.AllowHexSpecifier);
            // Get the exponent part
            byte exponentPart = (byte)(num >> 24);
            int exponent = (int)exponentPart - 128 - 24;

            uint fractionalPart = (num & 0x00FFFFFF) | (1U << 23);
            float fractionalDecimal = (float)fractionalPart;

            // Calculate the number
            float number = fractionalDecimal * (float)Math.Pow(2, exponent);
            //Console.WriteLine("Number for 0x{0:X}: {1}", num, number);
            float bqstudio_value;
            // Calculate the bqStudio values
            if (name_of_float == "CC Gain")
            {
                bqstudio_value = 8.4381f / number; //this conversion factor gives the same number as seen in BQstudio, for CC gain
            }
            else
            {
                bqstudio_value = 2517328.05f / number; //this conversion factor gives the same number as seen in BQstudio, for Capacity gain
            }
            return bqstudio_value;
        }
        static float BQ3060_HexStringToFloat(string hexString)
        {
            hexString = hexString.Replace(" ", "");
            uint num = uint.Parse(hexString, System.Globalization.NumberStyles.AllowHexSpecifier);
            // Get the exponent part
            byte exponentPart = (byte)(num >> 24);
            int exponent = (int)exponentPart - 128 - 24;

            uint fractionalPart = (num & 0x00FFFFFF) | (1U << 23);
            float fractionalDecimal = (float)fractionalPart;

            // Calculate the number
            float number = fractionalDecimal * (float)Math.Pow(2, exponent);
            float bqstudio_value = number;
            return bqstudio_value;
        }


        public static int CountBytes(string input)
        {
            // Split the string into an array of strings (bytes) using space as delimiter
            string[] bytes = input.Split(' ');

            // The number of bytes is equal to the number of substrings
            return bytes.Length;
        }


        public static List<read_help_pk_navi> Read_pk_navi_help(string filePath)
        {
            using (var reader = new StreamReader(filePath))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                var help_list = new List<read_help_pk_navi>();
                csv.Read();
                csv.ReadHeader();
                while (csv.Read())
                {
                    var record = new read_help_pk_navi
                    {
                        CLASS = csv.GetField("CLASS"),
                        SUBCLASS = csv.GetField("SUBCLASS"),
                        NAME = csv.GetField("NAME"),
                        ADDRESS = csv.GetField("ADDRESS"),
                        OFFSET = csv.GetField("OFFSET"),
                        NUM_READS = csv.GetField("NUM_READS"),
                        TYPE = csv.GetField("TYPE"),
                        UNIT = csv.GetField("UNIT")
                    };
                    help_list.Add(record);
                }
                return help_list;
            }
        }

        public static List<byte_data_pk_navi> Read_pk_navi_data(string battery_gauge_type)
        {
            var config = new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HasHeaderRecord = false,
                MissingFieldFound = null,
            };
            using (var byte_data = new StreamReader($"C:\\Users\\kodadason\\source\\repos\\battery_csv_bytes_conversion\\battery_csv_bytes_conversion\\{battery_gauge_type}_dataflash_read_examples.csv"))
            using (var csv = new CsvReader(byte_data, config))
            {
                int i = 0;
                var data_list = new List<byte_data_pk_navi>();
                while (csv.Read())
                {
                    if (i % 2 == 0)
                    {
                        var record = new byte_data_pk_navi
                        {
                            ADDRESS = csv.GetField(0),
                            DATA = csv.GetField(1)
                        };
                        data_list.Add(record);
                        int address_n = HexStringToInt(record.ADDRESS);

                    }
                    i++;
                }
                return data_list;
            }
        }


        static void parse_and_save_pk_navi(string battery_gauge_type)
        {
            var read_help = Read_pk_navi_help($"C:\\Users\\kodadason\\source\\repos\\battery_csv_bytes_conversion\\battery_csv_bytes_conversion\\{battery_gauge_type}_read_help.csv");
            var read_data = Read_pk_navi_data(battery_gauge_type);
            int df_address = 0;
            for (int k = 0; k < read_help.Count; k++)
            {
                var current_help = read_help[k];
                df_address = HexStringToInt(current_help.ADDRESS);
                int j = 0;
                while (j < read_data.Count)
                {
                    var raw_data_current = read_data[j];
                    int raw_data_address = HexStringToInt(raw_data_current.ADDRESS);
                    if (df_address == raw_data_address)
                    {
                        string type_string = current_help.TYPE;
                        string numberString = type_string.Substring(1); // Remove the first character 'S'
                        int type_size = int.Parse(numberString);
                        int from = int.Parse(current_help.OFFSET);
                        int to = from + type_size;
                        string raw_data_bytes = raw_data_current.DATA;
                        // Split the input string into individual byte substrings
                        string[] bytes = raw_data_bytes.Split(' ');
                        // Extract the desired range of bytes
                        string extract_bytes = string.Join(" ", bytes.Skip(from).Take(to - from));
                        string extract_bytes_rearranged = extract_bytes;
                        if (battery_gauge_type == "BQ4050")
                        {
                            // data from BQ4050 is stored little endian, except for strings in the dataflash
                            if (type_string[0] != 'S') extract_bytes_rearranged = ConvertEndianess(extract_bytes);
                        }
                        string measured_value = "";
                        if (type_string[0] == 'I') measured_value = $"{ConvertToSignedInt(extract_bytes_rearranged)}";
                        if (type_string[0] == 'U') measured_value = $"{ConvertToUnsignedInt(extract_bytes_rearranged)}";
                        if (type_string[0] == 'S') measured_value = $"{ConvertToAscii(extract_bytes_rearranged)}";
                        if (type_string[0] == 'H') measured_value = $"0x{extract_bytes_rearranged.Replace(" ", "")}";
                        if (type_string[0] == 'F')
                        {
                            if (battery_gauge_type == "BQ4050")
                            {
                                measured_value = $"{BQ4050_HexStringToFloat(extract_bytes_rearranged)}";
                            }
                            else
                            {
                                Console.WriteLine($"Hex to float test: {extract_bytes_rearranged} {current_help.UNIT}\n ------------- \n");
                                measured_value = $"{BQ78350_HexStringToFloat(extract_bytes_rearranged, current_help.NAME)}";
                            }
                            
                            Console.WriteLine($"Hex to float test: {measured_value} {current_help.UNIT}\n ------------- \n");
                        }
                        // Set the MeasuredValue property
                        current_help.MeasuredValue = measured_value;
                    }
                    j++;
                }

                using (var writer = new StreamWriter($"{battery_gauge_type}_parse_test.csv"))
                using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
                {
                    csv.WriteRecords(read_help);
                }
            }
            Console.WriteLine($"Done parsing and saving {battery_gauge_type} data to csv, press any key to continue.");
        }


        public static List<read_help_rheo> Read_rheo_help(string filePath) // BQ3060
        {
            using (var reader = new StreamReader(filePath))
            using (var csv = new CsvReader(reader, CultureInfo.InvariantCulture))
            {
                var help_list = new List<read_help_rheo>();
                csv.Read();
                csv.ReadHeader();
                while (csv.Read())
                {
                    var record = new read_help_rheo
                    {
                        CLASS = csv.GetField("CLASS"),
                        SUBCLASS = csv.GetField("SUBCLASS"),
                        NAME = csv.GetField("NAME"),
                        SUBCLASS_ID = csv.GetField("SUBCLASS_ID"),
                        OFFSET = csv.GetField("OFFSET"),
                        NUM_READS = csv.GetField("NUM_READS"),
                        TYPE = csv.GetField("TYPE"),
                        UNIT = csv.GetField("UNIT")
                    };
                    help_list.Add(record);
                }
                return help_list;
            }
        }

        public static List<byte_data_rheo> Read_rheo_data(string battery_gauge_type)
        {
            var config = new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HasHeaderRecord = false,
                MissingFieldFound = null,
            };
            using (var byte_data = new StreamReader($"C:\\Users\\kodadason\\source\\repos\\battery_csv_bytes_conversion\\battery_csv_bytes_conversion\\{battery_gauge_type}_dataflash_read_examples.csv"))
            using (var csv = new CsvReader(byte_data, config))
            {
                int i = 0;
                var data_list = new List<byte_data_rheo>();
                while (csv.Read())
                {
                    if (i % 2 == 0)
                    {
                        var record = new byte_data_rheo
                        {
                            SUBCLASS_ID = csv.GetField(0),
                            DATA = csv.GetField(1)
                        };
                        data_list.Add(record);
                    }
                    i++;
                }
                return data_list;
            }
        }


        static void parse_and_save_rheo(string battery_gauge_type)
        {
            var read_help = Read_rheo_help($"C:\\Users\\kodadason\\source\\repos\\battery_csv_bytes_conversion\\battery_csv_bytes_conversion\\{battery_gauge_type}_read_help.csv");
            var read_data = Read_rheo_data(battery_gauge_type);  
            int df_address = 0;
            for (int k = 0; k < read_help.Count; k++)
            {
                var current_help = read_help[k];
                df_address = int.Parse(current_help.SUBCLASS_ID);
                int j = 0;
                int visit_once = 0;
                while (j < read_data.Count)
                {
                    var raw_data_current = read_data[j];
                    int raw_data_address = HexStringToInt(raw_data_current.SUBCLASS_ID);
                    int number_reads = int.Parse(current_help.NUM_READS);
                    string raw_data_bytes = raw_data_current.DATA;
                    if (number_reads == 2 && j != read_data.Count - 1)
                    {
                        var next_raw_data = read_data[j + 1];
                        string next_raw_data_bytes = next_raw_data.DATA;
                        raw_data_bytes = string.Join("", raw_data_bytes, next_raw_data_bytes);
                    }
                    if (df_address == raw_data_address && visit_once == 0)
                    {
                        visit_once = 1;
                        string type_string = current_help.TYPE;
                        string numberString = type_string.Substring(1); // Remove the first character 'S'
                        int type_size = int.Parse(numberString);
                        int from = int.Parse(current_help.OFFSET);
                        int to = from + type_size;
                        // Split the input string into individual byte substrings
                        string[] bytes = raw_data_bytes.Split(' ');
                        // Extract the desired range of bytes
                        string extract_bytes = string.Join(" ", bytes.Skip(from).Take(to - from));
                        string extract_bytes_rearranged = extract_bytes;
                        string measured_value = "";
                        if (type_string[0] == 'I') measured_value = $"{ConvertToSignedInt(extract_bytes_rearranged)}";
                        if (type_string[0] == 'U') measured_value = $"{ConvertToUnsignedInt(extract_bytes_rearranged)}";
                        if (type_string[0] == 'S')
                        {

                            measured_value = $"{(ConvertToAscii(extract_bytes_rearranged).Replace("\n", string.Empty))}";
                        }
                        if (type_string[0] == 'H') measured_value = $"0x{extract_bytes_rearranged.Replace(" ", "")}";
                        if (type_string[0] == 'F')
                        {
                            measured_value = $"{BQ3060_HexStringToFloat(extract_bytes_rearranged)}";
                            Console.WriteLine($"Hex to float test: {measured_value} {current_help.UNIT}\n ------------- \n");
                        }
                        // Set the MeasuredValue property
                        current_help.MeasuredValue = measured_value;
                    }
                    
                    j++;
                }

                using (var writer = new StreamWriter($"{battery_gauge_type}_parse_test.csv"))
                using (var csv = new CsvWriter(writer, CultureInfo.InvariantCulture))
                {
                    csv.WriteRecords(read_help);
                }
            }
            Console.WriteLine($"Done parsing and saving {battery_gauge_type} data to csv, press any key to continue.");
        }




        static void Main(string[] args)
        {
            //parse_and_save_pk_navi("BQ4050");
            //Console.WriteLine($"Press any key to continue");
            //Console.ReadKey();
            //parse_and_save_pk_navi("BQ78350");
            //Console.WriteLine($"Press any key to continue");
            //Console.ReadKey();
            parse_and_save_rheo("BQ3060");
            Console.WriteLine($"Press any key to continue");
            Console.ReadKey();
        }
    }
}
