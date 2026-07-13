const String supabaseUrl = 'https://YOUR_SUPABASE_PROJECT_URL';
const String supabaseAnonKey = 'YOUR_SUPABASE_ANON_KEY';

bool get isSupabaseConfigured {
  return supabaseUrl.isNotEmpty &&
      !supabaseUrl.contains('YOUR_SUPABASE_PROJECT_URL') &&
      supabaseAnonKey.isNotEmpty &&
      !supabaseAnonKey.contains('YOUR_SUPABASE_ANON_KEY');
}
