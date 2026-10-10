import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { Calendar, MapPin, Users, Heart } from 'lucide-react'
import { format } from 'date-fns'
import { getEvents, addToWishlist } from '../lib/api'
import { useAuthStore } from '../lib/authStore'

export default function Events() {
  const { isAuthenticated } = useAuthStore()
  const { data: events = [], isLoading } = useQuery({
    queryKey: ['events'],
    queryFn: () => getEvents({ status: 'published' }),
  })

  const handleAddToWishlist = async (eventId: number) => {
    if (!isAuthenticated) {
      alert('Please login to add to wishlist')
      return
    }
    try {
      await addToWishlist(eventId)
      alert('Added to wishlist!')
    } catch (error) {
      console.error(error)
    }
  }

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <p>Loading events...</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">All Events</h1>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {events.map((event: any) => (
          <div key={event.id} className="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow overflow-hidden">
            <div className="h-48 bg-gradient-to-br from-primary-500 to-blue-600 relative">
              {event.is_featured && (
                <span className="absolute top-3 left-3 bg-yellow-500 text-white px-2 py-1 rounded text-xs font-semibold">Featured</span>
              )}
              <button
                onClick={() => handleAddToWishlist(event.id)}
                className="absolute top-3 right-3 p-2 bg-white/90 rounded-full hover:bg-white transition-colors"
              >
                <Heart className="h-4 w-4 text-gray-600" />
              </button>
            </div>
            <div className="p-6">
              <Link to={`/events/${event.id}`}>
                <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-primary-600">{event.title}</h3>
              </Link>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{event.short_description || event.description}</p>
              <div className="space-y-2 text-sm text-gray-500">
                <div className="flex items-center">
                  <Calendar className="h-4 w-4 mr-2" />
                  <span>{format(new Date(event.start_date), 'MMM dd, yyyy h:mm a')}</span>
                </div>
                {event.venue && (
                  <div className="flex items-center">
                    <MapPin className="h-4 w-4 mr-2" />
                    <span>{event.venue.city}, {event.venue.country}</span>
                  </div>
                )}
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Users className="h-4 w-4 mr-2" />
                    <span>{event.attendee_count || 0} attending</span>
                  </div>
                  <span className="text-lg font-bold text-primary-600">
                    {event.price === 0 ? 'Free' : `$${event.price}`}
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
