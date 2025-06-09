import os
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import statistics

class StatsAnalyzer:
    def __init__(self):
        self.results_file = os.path.expanduser("~/.terminal_typist_results.txt")
        self.json_file = os.path.expanduser("~/.terminal_typist_data.json")
        
    def save_detailed_result(self, stats, test_type):
        """Save detailed result in JSON format for analytics"""
        try:
            # Load existing data
            data = self._load_json_data()
            
            # Create new result entry
            result = {
                'timestamp': datetime.now().isoformat(),
                'date': datetime.now().strftime('%Y-%m-%d'),
                'test_type': test_type,
                'wpm': stats['wpm'],
                'accuracy': stats['accuracy'],
                'chars_typed': stats['chars_typed'],
                'correct_chars': stats['correct_chars'],
                'incorrect_chars': stats['incorrect_chars'],
                'time_taken': stats['time_taken'],
                'chars_per_second': stats['chars_per_second'],
                'error_rate': stats['error_rate'],
                'consistency': stats['consistency']
            }
            
            # Add to results
            data['results'].append(result)
            
            # Save back to file
            self._save_json_data(data)
            
        except Exception as e:
            # Silently fail if can't save
            pass
    
    def get_comprehensive_stats(self):
        """Get comprehensive statistics analysis"""
        data = self._load_json_data()
        results = data['results']
        
        if not results:
            return self._empty_stats()
        
        # Sort results by timestamp
        results.sort(key=lambda x: x['timestamp'])
        
        stats = {
            'total_tests': len(results),
            'total_time_spent': sum(r['time_taken'] for r in results),
            'total_chars_typed': sum(r['chars_typed'] for r in results),
            
            # WPM Statistics
            'top_5_wpm': self._get_top_5_wpm(results),
            'avg_wpm': round(statistics.mean(r['wpm'] for r in results), 1),
            'median_wpm': round(statistics.median(r['wpm'] for r in results), 1),
            'best_wpm': max(r['wpm'] for r in results),
            'worst_wpm': min(r['wpm'] for r in results),
            
            # Accuracy Statistics
            'avg_accuracy': round(statistics.mean(r['accuracy'] for r in results), 1),
            'best_accuracy': round(max(r['accuracy'] for r in results), 1),
            'worst_accuracy': round(min(r['accuracy'] for r in results), 1),
            
            # Streaks and Consistency
            'current_streak': self._calculate_current_streak(results),
            'longest_streak': self._calculate_longest_streak(results),
            'consistency_score': self._calculate_consistency_score(results),
            
            # Time-based Analytics
            'this_week_avg': self._get_period_average(results, 7),
            'this_month_avg': self._get_period_average(results, 30),
            'last_30_days_tests': self._get_period_test_count(results, 30),
            
            # Test Type Breakdown
            'test_type_stats': self._get_test_type_breakdown(results),
            
            # Progress Tracking
            'improvement_trend': self._calculate_improvement_trend(results),
            'recent_performance': self._get_recent_performance(results, 10),
            
            # Daily Statistics
            'best_day': self._get_best_day(results),
            'most_active_day': self._get_most_active_day(results),
            
            # Time of Day Analytics
            'peak_performance_time': self._get_peak_performance_time(results)
        }
        
        return stats
    
    def _load_json_data(self):
        """Load JSON data file"""
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        # Return default structure
        return {'results': []}
    
    def _save_json_data(self, data):
        """Save JSON data file"""
        try:
            with open(self.json_file, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def _empty_stats(self):
        """Return empty stats structure"""
        return {
            'total_tests': 0,
            'message': 'No tests completed yet. Start typing to see your statistics!'
        }
    
    def _get_top_5_wpm(self, results):
        """Get top 5 WPM scores with details"""
        sorted_results = sorted(results, key=lambda x: x['wpm'], reverse=True)[:5]
        return [
            {
                'wpm': r['wpm'],
                'accuracy': r['accuracy'],
                'date': r['date'],
                'test_type': r['test_type']
            }
            for r in sorted_results
        ]
    
    def _calculate_current_streak(self, results):
        """Calculate current daily streak"""
        if not results:
            return 0
        
        # Get unique dates
        dates = sorted(set(r['date'] for r in results), reverse=True)
        
        streak = 0
        current_date = datetime.now().date()
        
        for date_str in dates:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            if date_obj == current_date or date_obj == current_date - timedelta(days=streak):
                streak += 1
                current_date = date_obj - timedelta(days=1)
            else:
                break
        
        return streak
    
    def _calculate_longest_streak(self, results):
        """Calculate longest daily streak"""
        if not results:
            return 0
        
        dates = sorted(set(r['date'] for r in results))
        if not dates:
            return 0
        
        longest = 1
        current = 1
        
        for i in range(1, len(dates)):
            prev_date = datetime.strptime(dates[i-1], '%Y-%m-%d').date()
            curr_date = datetime.strptime(dates[i], '%Y-%m-%d').date()
            
            if curr_date - prev_date == timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        return longest
    
    def _calculate_consistency_score(self, results):
        """Calculate consistency score based on WPM variance"""
        if len(results) < 2:
            return 100
        
        wpms = [r['wpm'] for r in results]
        avg_wpm = statistics.mean(wpms)
        
        if avg_wpm == 0:
            return 0
        
        # Calculate coefficient of variation (lower is more consistent)
        cv = statistics.stdev(wpms) / avg_wpm * 100
        
        # Convert to consistency score (higher is better)
        consistency = max(0, 100 - cv)
        return round(consistency, 1)
    
    def _get_period_average(self, results, days):
        """Get average WPM for specified period"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_results = [
            r for r in results 
            if datetime.fromisoformat(r['timestamp']) >= cutoff_date
        ]
        
        if not recent_results:
            return 0
        
        return round(statistics.mean(r['wpm'] for r in recent_results), 1)
    
    def _get_period_test_count(self, results, days):
        """Get test count for specified period"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        return len([
            r for r in results 
            if datetime.fromisoformat(r['timestamp']) >= cutoff_date
        ])
    
    def _get_test_type_breakdown(self, results):
        """Get breakdown by test type"""
        type_stats = defaultdict(list)
        
        for result in results:
            type_stats[result['test_type']].append(result['wpm'])
        
        breakdown = {}
        for test_type, wpms in type_stats.items():
            breakdown[test_type] = {
                'count': len(wpms),
                'avg_wpm': round(statistics.mean(wpms), 1),
                'best_wpm': max(wpms)
            }
        
        return breakdown
    
    def _calculate_improvement_trend(self, results):
        """Calculate improvement trend"""
        if len(results) < 10:
            return "Need more tests"
        
        # Compare first 10 and last 10 tests
        first_10 = results[:10]
        last_10 = results[-10:]
        
        first_avg = statistics.mean(r['wpm'] for r in first_10)
        last_avg = statistics.mean(r['wpm'] for r in last_10)
        
        improvement = last_avg - first_avg
        
        if improvement > 5:
            return f"↗️ Improving (+{improvement:.1f} WPM)"
        elif improvement < -5:
            return f"↘️ Declining ({improvement:.1f} WPM)"
        else:
            return "↔️ Stable"
    
    def _get_recent_performance(self, results, count):
        """Get recent performance summary"""
        recent = results[-count:] if len(results) >= count else results
        
        if not recent:
            return {}
        
        return {
            'avg_wpm': round(statistics.mean(r['wpm'] for r in recent), 1),
            'avg_accuracy': round(statistics.mean(r['accuracy'] for r in recent), 1),
            'test_count': len(recent)
        }
    
    def _get_best_day(self, results):
        """Get best performing day"""
        if not results:
            return "No data"
        
        day_stats = defaultdict(list)
        for result in results:
            day_stats[result['date']].append(result['wpm'])
        
        best_date = max(day_stats.keys(), key=lambda d: statistics.mean(day_stats[d]))
        best_avg = round(statistics.mean(day_stats[best_date]), 1)
        
        return f"{best_date} ({best_avg} WPM avg)"
    
    def _get_most_active_day(self, results):
        """Get most active day"""
        if not results:
            return "No data"
        
        day_counts = Counter(r['date'] for r in results)
        most_active = day_counts.most_common(1)[0]
        
        return f"{most_active[0]} ({most_active[1]} tests)"
    
    def _get_peak_performance_time(self, results):
        """Get peak performance time of day"""
        if not results:
            return "No data"
        
        hour_stats = defaultdict(list)
        
        for result in results:
            hour = datetime.fromisoformat(result['timestamp']).hour
            hour_stats[hour].append(result['wpm'])
        
        if not hour_stats:
            return "No data"
        
        peak_hour = max(hour_stats.keys(), key=lambda h: statistics.mean(hour_stats[h]))
        peak_avg = round(statistics.mean(hour_stats[peak_hour]), 1)
        
        # Convert to readable time
        time_str = f"{peak_hour:02d}:00"
        return f"{time_str} ({peak_avg} WPM avg)"