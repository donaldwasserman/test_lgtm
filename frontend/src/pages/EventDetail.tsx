import { useParams } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Calendar, MapPin, Users, Globe, Heart, Star } from 'lucide-react'
import { format } from 'date-fns'
import { getEvent, createRsvp, addToWishlist, createReview, getEventReviews } from '../lib/api'
import { useAuthStore } from '../lib/authStore'
import { useState } from 'react'

export default function EventDetail() {
  const { id } = useParams<{ id: string }>()
  const { isAuthenticated, user } = useAuthStore()
  const queryClient = useQueryClient()
  const [rating, setRating] = useState(5)
  const [comment, setComment] = useState('')

  const { data: event, isLoading } = useQuery({
    queryKey: ['event', id],
    queryFn: () => getEvent(id!),
    enabled: !!id,
  })

  const { data: reviews = [] } = useQuery({
    queryKey: ['reviews', id],
    queryFn: () => getEventReviews(id!),
    enabled: !!id,
  })

  const rsvpMutation = useMutation({
    mutationFn: createRsvp,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['event', id] })
      alert('RSVP updated!')
    },
  })

  const wishlistMutation = useMutation({
    mutationFn: addToWishlist,
    onSuccess: () => {
      alert('Added to wishlist!')
    },
  })

  const reviewMutation = useMutation({
    mutationFn: createReview,
    onSuccess: () => {
      setComment('')
      queryClient.invalidateQueries({ queryKey: ['reviews', id] })
      alert('Review submitted!')
    },
  })

  const handleRsvp = (status: string) => {
    if (!isAuthenticated) {
      alert('Please login to RSVP')
      return
    }
    rsvpMutation.mutate({ event_id: parseInt(id!), status })
  }

  const handleWishlist = () => {
    if (!isAuthenticated) {
      alert('Please login to add to wishlist')
      return
    }
    wishlistMutation.mutate(parseInt(id!))
  }

  const handleReview = (e: React.FormEvent) => {
    e.preventDefault()
    if (!isAuthenticated) {
      alert('Please login to leave a review')
      return
    }
    reviewMutation.mutate({ event_id: parseInt(id!), rating, comment })
  }

  if (isLoading || !event) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="h-64 bg-gradient-to-br from-primary-600 to-blue-700"></div>
        <div className="p-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{event.title}</h1>
              {event.is_featured && <span className="bg-yellow-500 text-white px-3 py-1 rounded-full text-sm font-semibold">Featured</span>}
            </div>
            <button onClick={handleWishlist} className="flex items-center space-x-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
              <Heart className="h-5 w-5" />
              <span>Add to Wishlist</span>
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <h2 className="text-xl font-semibold mb-4">About this event</h2>
              <p className="text-gray-700 whitespace-pre-wrap mb-6">{event.description}</p>

              <h2 className="text-xl font-semibold mb-4">Reviews</h2>
              <div className="space-y-4 mb-6">
                {reviews.map((review: any) => (
                  <div key={review.id} className="border-b pb-4">
                    <div className="flex items-center space-x-2 mb-2">
                      {[...Array(5)].map((_, i) => (
                        <Star key={i} className={`h-4 w-4 ${i < review.rating ? 'text-yellow-500 fill-current' : 'text-gray-300'}`} />
                      ))}
                    </div>
                    {review.comment && <p className="text-gray-700">{review.comment}</p>}
                  </div>
                ))}
                {reviews.length === 0 && <p className="text-gray-500">No reviews yet. Be the first to review!</p>}
              </div>

              {isAuthenticated && (
                <form onSubmit={handleReview} className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="font-semibold mb-4">Leave a Review</h3>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Rating</label>
                    <select
                      value={rating}
                      onChange={(e) => setRating(parseInt(e.target.value))}
                      className="border rounded px-3 py-2"
                    >
                      <option value="5">5 Stars</option>
                      <option value="4">4 Stars</option>
                      <option value="3">3 Stars</option>
                      <option value="2">2 Stars</option>
                      <option value="1">1 Star</option>
                    </select>
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Comment</label>
                    <textarea
                      value={comment}
                      onChange={(e) => setComment(e.target.value)}
                      className="w-full border rounded px-3 py-2"
                      rows={3}
                    ></textarea>
                  </div>
                  <button type="submit" className="bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700">
                    Submit Review
                  </button>
                </form>
              )}
            </div>

            <div>
              <div className="bg-gray-50 p-6 rounded-lg mb-6">
                <h3 className="font-semibold mb-4">Event Details</h3>
                <div className="space-y-3">
                  <div className="flex items-start">
                    <Calendar className="h-5 w-5 text-gray-400 mr-3 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Start</p>
                      <p className="text-sm text-gray-600">{format(new Date(event.start_date), 'MMM dd, yyyy h:mm a')}</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <Calendar className="h-5 w-5 text-gray-400 mr-3 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">End</p>
                      <p className="text-sm text-gray-600">{format(new Date(event.end_date), 'MMM dd, yyyy h:mm a')}</p>
                    </div>
                  </div>
                  {event.venue && (
                    <div className="flex items-start">
                      <MapPin className="h-5 w-5 text-gray-400 mr-3 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">Location</p>
                        <p className="text-sm text-gray-600">{event.venue.name}</p>
                        <p className="text-sm text-gray-600">{event.venue.address}, {event.venue.city}</p>
                      </div>
                    </div>
                  )}
                  {event.is_virtual && event.virtual_link && (
                    <div className="flex items-start">
                      <Globe className="h-5 w-5 text-gray-400 mr-3 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">Virtual</p>
                        <a href={event.virtual_link} target="_blank" rel="noopener noreferrer" className="text-sm text-primary-600 hover:underline">
                          Join Link
                        </a>
                      </div>
                    </div>
                  )}
                  <div className="flex items-start">
                    <Users className="h-5 w-5 text-gray-400 mr-3 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">Attendees</p>
                      <p className="text-sm text-gray-600">{event.attendee_count || 0} / {event.max_attendees || 'Unlimited'}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-gray-50 p-6 rounded-lg">
                <div className="text-center mb-4">
                  <p className="text-3xl font-bold text-primary-600">{event.price === 0 ? 'Free' : `$${event.price}`}</p>
                </div>
                <div className="space-y-2">
                  <button onClick={() => handleRsvp('attending')} className="w-full bg-primary-600 text-white py-3 rounded-lg font-semibold hover:bg-primary-700">
                    RSVP Attending
                  </button>
                  <button onClick={() => handleRsvp('maybe')} className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50">
                    Maybe
                  </button>
                  <button onClick={() => handleRsvp('not_attending')} className="w-full border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-50">
                    Not Attending
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
