import { useQuery } from '@tanstack/react-query'
import { Calendar, Users, TrendingUp } from 'lucide-react'
import { getDashboardStats, getMyRsvps, getWishlist } from '../lib/api'

export default function Dashboard() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: getDashboardStats,
  })
  const { data: rsvps = [] } = useQuery({
    queryKey: ['my-rsvps'],
    queryFn: getMyRsvps,
  })
  const { data: wishlist = [] } = useQuery({
    queryKey: ['wishlist'],
    queryFn: getWishlist,
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Calendar className="h-8 w-8 text-primary-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-500">My Events</p>
              <p className="text-2xl font-bold">{stats?.total_events || 0}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <Users className="h-8 w-8 text-green-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-500">Total Attendees</p>
              <p className="text-2xl font-bold">{stats?.total_attendees || 0}</p>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <TrendingUp className="h-8 w-8 text-blue-600" />
            <div className="ml-4">
              <p className="text-sm text-gray-500">Published</p>
              <p className="text-2xl font-bold">{stats?.published_events || 0}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold mb-4">My RSVPs</h2>
          {rsvps.length === 0 ? (
            <p className="text-gray-500">No RSVPs yet</p>
          ) : (
            <div className="space-y-3">
              {rsvps.slice(0, 5).map((rsvp: any) => (
                <div key={rsvp.id} className="flex justify-between items-center py-2 border-b">
                  <span className="text-sm">Event #{rsvp.event_id}</span>
                  <span className="text-sm font-medium capitalize">{rsvp.status}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold mb-4">Wishlist</h2>
          {wishlist.length === 0 ? (
            <p className="text-gray-500">Nothing in wishlist</p>
          ) : (
            <div className="space-y-3">
              {wishlist.slice(0, 5).map((item: any) => (
                <div key={item.id} className="py-2 border-b">
                  <span className="text-sm">Event #{item.event_id}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
